import threading
import time
from collections import defaultdict

import pydivert

from src.cores.base import BaseEngine
from src.utils.helpers import get_protocol_name, log_to_file


class WindowsEngine(BaseEngine):
    def __init__(self, rules, website_filter, parent=None):
        super().__init__(rules, website_filter, parent)
        self.traffic_tracker = defaultdict(list)
        self.whitelist = ["127.0.0.1", "::1"]
        self.blacklist = set()

    def remove_from_blacklist(self, ip, timeout=60):
        time.sleep(timeout)
        if ip in self.blacklist:
            self.blacklist.remove(ip)
            self.rules_signal.emit(f"Removed from Black List: {ip}")
            log_to_file(f"Removed from Black List: {ip}", level="info")

    def run(self):
        try:
            with pydivert.WinDivert("tcp or udp") as w:
                for packet in w:
                    if not self.running:
                        break

                    src_ip = packet.src_addr
                    dst_ip = packet.dst_addr
                    protocol = get_protocol_name(packet.protocol)
                    current_time = time.time()

                    self.log_signal.emit(src_ip, dst_ip, protocol)
                    log_to_file(f"Packet Seen: {src_ip}:{packet.src_port} -> {dst_ip}:{packet.dst_port}")

                    if src_ip in self.whitelist:
                        w.send(packet)
                        continue

                    if src_ip in self.blacklist:
                        self.rules_signal.emit(f"IP in Black List! Dropping {src_ip}")
                        continue

                    if dst_ip in self.website_filter:
                        self.rules_signal.emit(f"Blocked by Website Filter: {dst_ip}")
                        log_to_file(f"Blocked Website Packet: {dst_ip}", level="warning")
                        continue

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
                        continue

                    blocked = False
                    for rule in self.rules:
                        rule_lower = rule.lower()

                        if rule_lower == "tcp" and protocol.lower() == "tcp":
                            self.rules_signal.emit("TCP Packet Blocked by Rule!")
                            log_to_file(
                                f"Blocked TCP: {src_ip}:{packet.src_port} -> {dst_ip}:{packet.dst_port}",
                                level="warning",
                            )
                            blocked = True
                            break

                        if rule_lower == "udp" and protocol.lower() == "udp":
                            self.rules_signal.emit("UDP Packet Blocked by Rule!")
                            log_to_file(
                                f"Blocked UDP: {src_ip}:{packet.src_port} -> {dst_ip}:{packet.dst_port}",
                                level="warning",
                            )
                            blocked = True
                            break

                        if rule.startswith(":"):
                            try:
                                port_num = int(rule.replace(":", ""))
                                if packet.src_port == port_num or packet.dst_port == port_num:
                                    self.rules_signal.emit(f"Packet Blocked by Port Rule {rule}")
                                    log_to_file(
                                        f"Blocked by Port {rule}: "
                                        f"{src_ip}:{packet.src_port} -> {dst_ip}:{packet.dst_port}",
                                        level="warning",
                                    )
                                    blocked = True
                                    break
                            except ValueError:
                                pass

                        if ":" in rule:
                            if rule == f"{packet.src_addr}:{packet.src_port}":
                                self.rules_signal.emit(f"Packet Blocked by IP:Port Rule {rule}")
                                log_to_file(f"Blocked by IP:Port {rule}", level="warning")
                                blocked = True
                                break
                            if rule == f"{packet.dst_addr}:{packet.dst_port}":
                                self.rules_signal.emit(f"Packet Blocked by IP:Port Rule {rule}")
                                log_to_file(f"Blocked by IP:Port {rule}", level="warning")
                                blocked = True
                                break

                    if blocked:
                        continue

                    w.send(packet)

        except Exception as e:
            self.rules_signal.emit(f"Firewall Error: {e}")
            log_to_file(f"Firewall Error: {e}", level="error")

    def stop(self):
        self.running = False
