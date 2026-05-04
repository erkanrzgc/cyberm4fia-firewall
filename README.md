<h1 align="center">cyberm4fia-firewall</h1>

<p align="center">
  <img src="https://img.shields.io/badge/mission-kernel%20level%20packet%20control-red?style=for-the-badge" alt="mission">
</p>

<table align="center"><tr><td valign="middle">
<pre>
 ██████ ██    ██ ██████  ███████ ██████  ███    ███ ██   ██ ███████ ██  █████  
██       ██  ██  ██   ██ ██      ██   ██ ████  ████ ██   ██ ██      ██ ██   ██ 
██        ████   ██████  █████   ██████  ██ ████ ██ ███████ █████   ██ ███████ 
██         ██    ██   ██ ██      ██   ██ ██  ██  ██      ██ ██      ██ ██   ██ 
 ██████    ██    ██████  ███████ ██   ██ ██      ██      ██ ██      ██ ██   ██ 
</pre>
</td><td valign="middle">
<img src="https://raw.githubusercontent.com/erkanrzgc/ai-house/main/resources/icons/icon_256.png" width="150">
</td></tr></table>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue?style=flat-square&logo=python" alt="python">
  <img src="https://img.shields.io/badge/platform-windows%20%7C%20linux-purple?style=flat-square" alt="platform">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="license">
  <img src="https://img.shields.io/badge/engines-NFQUEUE%20%7C%20WinDivert-orange?style=flat-square" alt="engines">
  <img src="https://img.shields.io/github/last-commit/erkanrzgc/firewall?style=flat-square" alt="last commit">
</p>

<p align="center">
  <b>cyberm4fia-firewall</b> is a cross-platform real-time packet filtering engine with a dark-theme PyQt5 GUI, featuring kernel-level traffic interception, DDoS protection, and website blocking — for both Windows and Linux.
</p>

---

## Features

### Packet Interception & Filtering
| Capability | Engine | Description |
|---|---|---|
| TCP/UDP Capture | NFQUEUE · WinDivert | Kernel-level packet interception on all interfaces |
| Protocol Blocking | `tcp` `udp` rules | Block entire protocol families with a single rule |
| Port Filtering | `:80` `:443` `:22` | Src/dst port matching for granular control |
| IP:Port Rules | `192.168.1.1:443` | Pinpoint blocking of specific endpoints |
| Website Blocking | DNS-resolved domains | Enter URL → resolve to IP → block all traffic |

### Defense & Monitoring
| Feature | Mechanism | Description |
|---|---|---|
| DDoS Protection | 10k/1s · 50k/10s thresholds | Auto-blacklist offending IPs for 60 seconds |
| Real-Time GUI | PyQt5 QThread architecture | Non-blocking UI with live traffic table |
| Event Logging | `logs/firewall.log` | Full audit trail of all packets and actions |
| Whitelist | `127.0.0.1` `::1` | Localhost traffic always permitted |

### Cross-Platform Engine
| Platform | Backend | Kernel Interface |
|---|---|---|
| 🐧 Linux | `src/cores/linux.py` | iptables NFQUEUE + scapy packet parser |
| 🪟 Windows | `src/cores/windows.py` | WinDivert driver + pydivert bindings |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     firewall.py (entry)                      │
│              Root check · Locale · Launch                    │
└───────────────────────────┬──────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │   src/main.py   │
                    │  QApplication   │
                    │  GUI Bootstrap  │
                    └───────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
     ┌────────▼──────┐ ┌───▼────┐ ┌──────▼──────┐
     │  src/gui.py   │ │ src/  │ │  src/cores/ │
     │  FirewallGUI  │ │styles │ │  ┌─────────┐│
     │  (QMainWindow)│ │ .py   │ │  │ base.py ││
     └───────┬───────┘ └───────┘ │  │ (Engine)││
             │                   │  ├─────────┤│
             │  create_engine()  │  │linux.py ││ ─── NFQUEUE + scapy + iptables
             └─────────────────► │  ├─────────┤│
                                 │  │win.py   ││ ─── pydivert / WinDivert
                                 │  └─────────┘│
                                 └─────────────┘
```

### Linux Packet Flow

```
Network Stack → iptables (NFQUEUE) → Queue #0 → Python Callback
                                                        │
                                              ┌─────────┴─────────┐
                                              │                   │
                                         ACCEPT (allow)      DROP (block)
```

**iptables rules — auto-added on start, cleaned up on stop:**

```bash
iptables -A INPUT  -p tcp -j NFQUEUE --queue-num 0 --queue-bypass
iptables -A INPUT  -p udp -j NFQUEUE --queue-num 0 --queue-bypass
iptables -A OUTPUT -p tcp -j NFQUEUE --queue-num 0 --queue-bypass
iptables -A OUTPUT -p udp -j NFQUEUE --queue-num 0 --queue-bypass
```

---

## Quick Start

### 🐧 Linux

```bash
sudo apt install python3-pyqt5 python3-scapy python3-netfilterqueue iptables
git clone https://github.com/erkanrzgc/firewall.git
cd firewall
sudo python3 firewall.py
```

### 🪟 Windows

```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python firewall.py
```

> **Windows requires** [WinDivert](https://github.com/basil00/Divert/releases) driver. Copy `WinDivert.dll` to `C:\Windows\System32`.

---

## Usage

### Rule Format

| Type | Syntax | Example | Blocks |
|------|--------|---------|--------|
| Protocol | `tcp` | `tcp` | All TCP traffic |
| Protocol | `udp` | `udp` | All UDP traffic |
| Port | `:PORT` | `:80` | Src or dst port 80 |
| Port (short) | `PORT` | `443` | Auto → `:443` |
| IP:Port | `IP:PORT` | `192.168.1.5:22` | Specific IP + port |

### GUI Sections

| Section | What It Shows |
|---------|---------------|
| **Start / Stop** | Toggle packet capture. Enables/disables kernel rules. |
| **Rules** | Add, view, delete filtering rules with validation. |
| **Network Traffic** | Real-time table — Source IP, Destination IP, Protocol. |
| **Applied Rules** | Scrollable event log — blocks, DDoS detections, rule changes. |
| **Blocked Websites** | Domain → resolved IP → blacklist with display. |

---

## Project Structure

```
cyberm4fia-firewall/
│
├── firewall.py              Entry point (sudo python3 firewall.py)
├── assets/
│   └── icon.png             Application icon (256×256)
├── logs/
│   └── .gitkeep             Runtime log directory
├── src/
│   ├── main.py              QApplication bootstrap + launcher
│   ├── gui.py               FirewallGUI (QMainWindow)
│   ├── styles.py            QSS dark theme stylesheet
│   ├── cores/
│   │   ├── __init__.py      create_engine() factory
│   │   ├── base.py          BaseEngine (abstract QThread)
│   │   ├── linux.py         Linux engine — NFQUEUE + scapy + iptables
│   │   └── windows.py       Windows engine — pydivert / WinDivert
│   └── utils/
│       └── helpers.py       Logging · PROTOCOL_MAP · resolvers
├── requirements.txt         Dependencies
├── README.md
└── LICENSE                  MIT License
```

---

## Configuration

Settings in `src/cores/linux.py` / `src/cores/windows.py`:

| Threshold | Default | Description |
|-----------|---------|-------------|
| `SHORT_WINDOW` | 10000 | Packets per second for DDoS detection |
| `LONG_WINDOW` | 50000 | Packets per 10 seconds for DDoS detection |
| `BLACKLIST_TIMEOUT` | 60 | Seconds before IP auto-removal |
| `whitelist` | `127.0.0.1` `::1` | Always-permitted addresses |

UI styling in `src/styles.py` — colors, fonts, padding, hover effects.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `sudo` required | `sudo python3 firewall.py` |
| `iptables` not found | `sudo apt install iptables` |
| `NetfilterQueue` import error | `pip install NetfilterQueue` or `apt install python3-netfilterqueue` |
| GUI won't start | Check `$DISPLAY` is set |
| No traffic captured | `sudo iptables -L -n \| grep NFQUEUE` |
| Logs not writing | Verify `logs/` directory permissions |

---

## License

MIT License — see [LICENSE](./LICENSE) for details.

<sub>Copyright (c) 2025 · ERKAN RISNGITS</sub>
