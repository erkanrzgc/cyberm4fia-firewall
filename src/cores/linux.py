import subprocess
import threading
import time
from collections import defaultdict

from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, UDP

from src.cores.base import BaseEngine
from src.utils.helpers import get_protocol_name, log_to_file


class LinuxEngine(BaseEngine):
    def __init__(self, rules, website_filter, parent=None):
        super().__init__(rules, website_filter, parent)
        self.traffic_tracker = defaultdict(list)
        self.whitelist = ["127.0.0.1", "::1"]
        self.blacklist = set()
        self.nfqueue = None

    def remove_from_blacklist(self, ip, timeout=60):
        time.sleep(timeout)
        if ip in self.blacklist:
            self.blacklist.remove(ip)
            self.rules_signal.emit(f"Removed from Black List: {ip}")
            log_to_file(f"Removed from Black List: {ip}", level="info")

    def setup_iptables(self):
        for chain in ("INPUT", "OUTPUT"):
            for proto in ("tcp", "udp"):
                subprocess.run(
                    [
                        "iptables", "-A", chain, "-p", proto,
                        "-j", "NFQUEUE", "--queue-num", "0", "--queue-bypass",
                    ],
                    check=True,
                    capture_output=True,
                )
        self.rules_signal.emit("iptables NFQUEUE rules added (INPUT + OUTPUT)")

    def cleanup_iptables(self):
        for chain in ("INPUT", "OUTPUT"):
            for proto in ("tcp", "udp"):
                try:
                    subprocess.run(
                        [
                            "iptables", "-D", chain, "-p", proto,
                            "-j", "NFQUEUE", "--queue-num", "0", "--queue-bypass",
                        ],
                        capture_output=True,
                    )
                except Exception:
                    pass
        self.rules_signal.emit("iptables NFQUEUE rules cleaned up")

    def _callback(self, nfpacket):
        if not self.running:
            nfpacket.accept()
            if self.nfqueue is not None:
                self.nfqueue.unbind()
            return

        raw = nfpacket.get_payload()
        try:
            pkt = IP(raw)
        except Exception:
            nfpacket.accept()
            return

        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        protocol_num = pkt[IP].proto
        protocol = get_protocol_name(protocol_num)

        src_port = dst_port = 0
        if protocol_num == 6 and TCP in pkt:
            src_port = pkt[TCP].sport
            dst_port = pkt[TCP].dport
        elif protocol_num == 17 and UDP in pkt:
            src_port = pkt[UDP].sport
            dst_port = pkt[UDP].dport

        self.log_signal.emit(src_ip, dst_ip, protocol)
        log_to_file(f"Packet Seen: {src_ip}:{src_port} -> {dst_ip}:{dst_port}")

        if self._apply_rules(src_ip, dst_ip, src_port, dst_port, protocol):
            nfpacket.drop()
        else:
            nfpacket.accept()

    def _apply_rules(self, src_ip, dst_ip, src_port, dst_port, protocol):
        current_time = time.time()

        if src_ip in self.whitelist or dst_ip in self.whitelist:
            return False

        if src_ip in self.blacklist:
            self.rules_signal.emit(f"IP in Black List! Dropping {src_ip}")
            return True

        if dst_ip in self.website_filter:
            self.rules_signal.emit(f"Blocked by Website Filter: {dst_ip}")
            log_to_file(f"Blocked Website Packet: {dst_ip}", level="warning")
            return True

        self.traffic_tracker[src_ip].append(current_time)
        short_window = [ts for ts in self.traffic_tracker[src_ip] if current_time - ts <= 1]
        long_window = [ts for ts in self.traffic_tracker[src_ip] if current_time - ts <= 10]
        self.traffic_tracker[src_ip] = long_window

        if len(short_window) > 10000 or len(long_window) > 50000:
            self.rules_signal.emit(
                f"DDoS detected! Blacklisting {src_ip} "
                f"(1s={len(short_window)},10s={len(long_window)})"
            )
            self.blacklist.add(src_ip)
            log_to_file(f"DDoS Detected and Blocked: {src_ip}", level="warning")
            threading.Thread(target=self.remove_from_blacklist, args=(src_ip,)).start()
            return True

        for rule in self.rules:
            rule_lower = rule.lower()

            if rule_lower == "tcp" and protocol.lower() == "tcp":
                self.rules_signal.emit("TCP Packet Blocked by Rule!")
                log_to_file(f"Blocked TCP: {src_ip}:{src_port} -> {dst_ip}:{dst_port}", level="warning")
                return True

            if rule_lower == "udp" and protocol.lower() == "udp":
                self.rules_signal.emit("UDP Packet Blocked by Rule!")
                log_to_file(f"Blocked UDP: {src_ip}:{src_port} -> {dst_ip}:{dst_port}", level="warning")
                return True

            if rule.startswith(":"):
                try:
                    port_num = int(rule.replace(":", ""))
                    if src_port == port_num or dst_port == port_num:
                        self.rules_signal.emit(f"Packet Blocked by Port Rule {rule}")
                        log_to_file(
                            f"Blocked by Port {rule}: {src_ip}:{src_port} -> {dst_ip}:{dst_port}",
                            level="warning",
                        )
                        return True
                except ValueError:
                    pass

            if ":" in rule:
                if rule == f"{src_ip}:{src_port}" or rule == f"{dst_ip}:{dst_port}":
                    self.rules_signal.emit(f"Packet Blocked by IP:Port Rule {rule}")
                    log_to_file(f"Blocked by IP:Port {rule}", level="warning")
                    return True

        return False

    def run(self):
        try:
            self.setup_iptables()
            self.nfqueue = NetfilterQueue()
            self.nfqueue.bind(0, self._callback)
            self.nfqueue.run()
        except Exception as e:
            if self.running:
                self.rules_signal.emit(f"Firewall Error: {e}")
                log_to_file(f"Firewall Error: {e}", level="error")
        finally:
            self.cleanup_iptables()

    def stop(self):
        self.running = False
        if self.nfqueue is not None:
            try:
                self.nfqueue.unbind()
            except Exception:
                import socket as _sock
                s = _sock.socket(_sock.AF_INET, _sock.SOCK_DGRAM)
                try:
                    s.sendto(b"", ("127.0.0.1", 9))
                except Exception:
                    pass
                finally:
                    s.close()
        self.wait()
