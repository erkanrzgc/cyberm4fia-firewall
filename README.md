<div align="center">

```
 _______   _______ ______________  ___  ___ ______ _____  ___  
/  __ \ \ / / ___ \  ___| ___ \  \/  | /   ||  ___|_   _|/ _ \ 
| /  \/\ V /| |_/ / |__ | |_/ / .  . |/ /| || |_    | | / /_\ \
| |     \ / | ___ \  __||    /| |\/| / /_| ||  _|   | | |  _  |
| \__/\ | | | |_/ / |___| |\ \| |  | \___  || |    _| |_| | | |
 \____/ \_/ \____/\____/\_| \_\_|  |_/   |_/\_|    \___/\_| |_/

</div>

<div align="center">

[![Python](https://img.shields.io/badge/python-3.11+-blue?style=flat-square&logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux-purple?style=flat-square)](https://github.com/erkanrzgc/firewall)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-darkgreen?style=flat-square)](https://riverbankcomputing.com/software/pyqt)
[![Linux Engine](https://img.shields.io/badge/engine-NFQUEUE%20%2B%20scapy-orange?style=flat-square)](./src/cores/linux.py)
[![Windows Engine](https://img.shields.io/badge/engine-WinDivert%20%2B%20pydivert-blue?style=flat-square)](./src/cores/windows.py)

</div>

---

**cyberm4fia-firewall** is a cross-platform real-time packet filtering engine with a clean PyQt5 dark-theme GUI. Intercepts TCP/UDP traffic at the kernel level, applies user-defined rules, and blocks threats — works on both Windows and Linux with automatic platform detection.

---

## Features

| Category | Feature | Description |
|----------|---------|-------------|
| 🔥 **Packet Capture** | Kernel-level interception | Windows: WinDivert · Linux: iptables + NFQUEUE |
| 🚫 **Rule Engine** | Protocol · Port · IP:Port | `tcp` `udp` `:80` `192.168.1.1:443` |
| 🌐 **Website Blocker** | DNS-resolved domain blocking | Enter domain → resolves IP → blocks all traffic |
| ⚡ **DDoS Protection** | Automated blacklisting | 10k pkt/s or 50k pkt/10s → 60s ban |
| 🧵 **Multi-Threaded** | GUI + engine separation | PyQt5 QThread for non-blocking UI |
| 📝 **Logging** | Full event audit | Stored in `logs/firewall.log` |
| 🎨 **Dark UI** | Custom QSS theme | GitHub-dark inspired with CyberM4fia accents |
| 🔄 **Cross-Platform** | Auto engine selection | Detects OS at runtime, loads correct backend |

---

## Architecture

```
┌──────────────┐     create_engine()     ┌────────────────┐
│   src/gui.py  │ ─────────────────────▶ │  src/cores/    │
│  FirewallGUI  │                        │  __init__.py   │
│  (QMainWindow)│                        │  (Factory)     │
└──────────────┘                        └───────┬────────┘
                                                │
                     ╭──────────────────────────┼──────────────────────────╮
                     │                          │                          │
             ┌───────▼────────┐        ┌────────▼─────────┐
             │  src/cores/     │        │  src/cores/       │
             │  linux.py       │        │  windows.py       │
             │                 │        │                   │
             │  NetfilterQueue │        │  pydivert         │
             │  + scapy        │        │  + WinDivert      │
             │  + iptables     │        │                   │
             └───────┬────────┘        └───────────────────┘
                     │
                     │  🐧 Linux only
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
 ┌─────────┐  ┌──────────┐  ┌──────────┐
 │ iptables│  │ NFQUEUE  │  │  scapy   │
 │ rules   │  │ Queue 0  │  │  parser  │
 └─────────┘  └──────────┘  └──────────┘
```

### Linux Packet Flow

```
 Network → iptables → NFQUEUE → Python Callback → scapy IP parse
    │                                                    │
    │                                           ┌────────┴────────┐
    │                                           │                 │
    │                                      ACCEPT              DROP
    │                                     (forward)           (block)
    │                                         │                 │
    └─────────────────────────────────────────┘                 │
                                                               │
                                                        packet discarded
```

**iptables rules — auto-added on start:**

| Chain | Protocol | Action |
|-------|----------|--------|
| `INPUT` | tcp | `-j NFQUEUE --queue-num 0 --queue-bypass` |
| `INPUT` | udp | `-j NFQUEUE --queue-num 0 --queue-bypass` |
| `OUTPUT` | tcp | `-j NFQUEUE --queue-num 0 --queue-bypass` |
| `OUTPUT` | udp | `-j NFQUEUE --queue-num 0 --queue-bypass` |

All rules are cleaned up on stop. `--queue-bypass` ensures traffic flows normally if the app exits.

---

## Quick Start

### 🐧 Linux

```bash
# Install dependencies
sudo apt install python3-pyqt5 python3-scapy python3-netfilterqueue iptables

# Clone & run
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

| Type | Syntax | Example | Effect |
|------|--------|---------|--------|
| Protocol | `tcp` | `tcp` | Block all TCP traffic |
| Protocol | `udp` | `udp` | Block all UDP traffic |
| Port | `:PORT` | `:80` | Block src/dst port 80 |
| Port (short) | `PORT` | `443` | Auto-converted to `:443` |
| IP:Port | `IP:PORT` | `192.168.1.5:22` | Block specific IP + port |

### GUI Sections

| Section | Function |
|---------|----------|
| **Start / Stop** | Begin/end packet capture. Enables/disables iptables rules. |
| **Rules** | Add, view, delete filtering rules. |
| **Network Traffic** | Real-time table of captured packets (Src IP, Dst IP, Protocol). |
| **Applied Rules** | Scrollable log of all events, blocks, and DDoS detections. |
| **Blocked Websites** | Enter domain → resolved to IP → added to blacklist. |

---

## Project Structure

```
cyberm4fia-firewall/
│
├── firewall.py              Entry point (sudo python3 firewall.py)
├── assets/
│   └── icon.png             Application icon
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

```python
# DDoS thresholds
SHORT_WINDOW = 10000       # packets per second
LONG_WINDOW  = 50000       # packets per 10 seconds

# Blacklist auto-removal
BLACKLIST_TIMEOUT = 60     # seconds

# Whitelist (always permitted)
self.whitelist = ["127.0.0.1", "::1"]
```

UI styles in `src/styles.py` — colors, fonts, padding, hover effects.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `sudo: password required` | Run with `sudo python3 firewall.py` |
| `iptables: command not found` | `sudo apt install iptables` |
| `NetfilterQueue` import error | `pip install NetfilterQueue` or `apt install python3-netfilterqueue` |
| GUI won't start | Check `$DISPLAY`: `echo $DISPLAY` |
| No traffic captured | Verify rules: `sudo iptables -L -n \| grep NFQUEUE` |
| Logs not writing | Check `logs/firewall.log` permissions |

---

## License

MIT License — see [LICENSE](./LICENSE).

<div align="center">

```
  ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
  █  CyberM4fia Firewall · linux + windows · 2025  █
  ▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀ 
```

</div>
