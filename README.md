

████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
                                                                                                                    
$$\      $$\  $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\  $$\   $$\  $$$$$$\  $$\   $$\ $$$$$$$$\ $$$$$$$$\ 
$$$\    $$$ |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$$\  $$ |$$  __$$\ $$$\  $$ |$$  _____|$$  _____|
$$$$\  $$$$ |$$ /  $$ |$$ /  \__|$$ /  \__|$$ /  $$ |$$$$\ $$ |$$ /  $$ |$$$$\ $$ |$$ |      $$ |      
$$\$$\$$ $$ |$$$$$$$$ |$$ |      $$ |      $$ |  $$ |$$ $$\$$ |$$ |  $$ |$$ $$\$$ |$$$$$\    $$$$$\    
$$ \$$$  $$ |$$  __$$ |$$ |      $$ |      $$ |  $$ |$$ \$$$$ |$$ |  $$ |$$ \$$$$ |$$  __|   $$  __|   
$$ |\$  /$$ |$$ |  $$ |$$ |  $$\ $$ |  $$\ $$ |  $$ |$$ |\$$$ |$$ |  $$ |$$ |\$$$ |$$ |      $$ |      
$$ | \_/ $$ |$$ |  $$ |\$$$$$$  |\$$$$$$  | $$$$$$  |$$ | \$$ | $$$$$$  |$$ | \$$ |$$$$$$$$\ $$$$$$$$\ 
\__|     \__|\__|  \__| \______/  \______/  \______/ \__|  \__| \______/ \__|  \__|\________|\________|
                                                                                                        
                                                                                                        
                                    ╔══════════════════════════════════════╗
                                    ║       CROSS-PLATFORM FIREWALL        ║
                                    ║     Windows · Linux · PyQt5 GUI      ║
                                    ╚══════════════════════════════════════╝
████████████████████████████████████████████████████████████████████████████████████████████████████████████████████


Real-time packet capture, protocol/port/IP filtering, DDoS protection, and website blocking — all wrapped in a sleek dark-theme GUI.


## FEATURES

╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  🔥 Real-Time Packet Capture                                                 ║
║     Captures TCP/UDP traffic using platform-native engines                    ║
║     Windows → WinDivert (pydivert)                                          ║
║     Linux   → NetfilterQueue + scapy + iptables NFQUEUE                     ║
║                                                                              ║
║  🛡️ Protocol & Port Filtering                                                ║
║     Block by protocol (tcp / udp)                                            ║
║     Block by port (:80, :443, :22)                                           ║
║     Block by IP:Port combo (192.168.1.1:80)                                 ║
║                                                                              ║
║  🌐 Website Blocking                                                         ║
║     Enter a domain → resolves to IP → blocks all traffic                     ║
║                                                                              ║
║  🚫 DDoS Protection                                                          ║
║     10k packets/s or 50k packets/10s → auto-blacklist for 60s               ║
║                                                                              ║
║  🎨 Dark Theme GUI                                                           ║
║     PyQt5 dark interface with real-time traffic table                        ║
║     Applied rules log, blocklist manager                                     ║
║                                                                              ║
║  📝 Logging                                                                  ║
║     All events logged to firewall_logs.txt                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝


## PLATFORMS

  🪟 Windows 7+     │  🐧 Linux (Kali, Ubuntu, Debian, Arch, etc.)

  WinDivert backend  │  NetfilterQueue + scapy backend
  Administrator req. │  Root (sudo) required


## REQUIREMENTS

  • Python 3.7+
  • PyQt5

  Windows:
    • WinDivert driver
    • Administrator privileges

  Linux:
    • iptables
    • Root privileges
    • netfilter queue support (kernel module)


## INSTALLATION

### 🐧 Linux (Kali / Debian / Ubuntu)

  sudo apt install python3-pyqt5 python3-scapy python3-netfilterqueue
  git clone https://github.com/your-repo/cyberm4fia-firewall.git
  cd cyberm4fia-firewall
  sudo python3 firewall.py

  Or via pip:

  pip install -r requirements.txt
  sudo python3 firewall.py

### 🪟 Windows

  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  python firewall.py

  (Run as Administrator!)


## USAGE

### 🚀 Start / Stop

  Click "Start Firewall" to begin capturing packets.
  Click "Stop Firewall" to stop and clean up rules.

  On Linux, the app automatically:
    • Adds iptables NFQUEUE rules to INPUT and OUTPUT chains
    • Intercepts TCP/UDP packets for inspection
    • Cleans up iptables rules on stop

### 📜 Adding Rules

  ┌─────────────────────────────────────────────────────────────┐
  │  Rule Type          │  Example          │  Effect            │
  ├─────────────────────────────────────────────────────────────┤
  │  Protocol           │  tcp              │  Block all TCP     │
  │  Protocol           │  udp              │  Block all UDP     │
  │  Port               │  :80              │  Block port 80     │
  │  IP:Port            │  192.168.1.1:443  │  Block specific     │
  └─────────────────────────────────────────────────────────────┘

### 🌐 Blocking Websites

  Enter a domain (e.g., www.example.com) and click "Add Website."
  The app resolves it to an IP and blocks traffic to/from it.

### 🛡️ DDoS Protection

  Thresholds (configurable):
    • 10,000 packets in 1 second → blacklist
    • 50,000 packets in 10 seconds → blacklist
    • Auto-removed from blacklist after 60 seconds


## ARCHITECTURE

```
  firewall/
  │
  ├── firewall.py           Entry point (root check, locale, launcher)
  ├── engine.py             BaseEngine class + platform factory
  ├── engine_linux.py       Linux engine (NetfilterQueue + scapy)
  ├── engine_windows.py     Windows engine (pydivert / WinDivert)
  ├── gui.py                PyQt5 GUI (FirewallGUI)
  ├── styles.py             QSS dark theme stylesheet
  ├── icon.png              Application icon (shield)
  ├── requirements.txt      Dependencies
  ├── firewall_logs.txt     Runtime logs (auto-generated)
  ├── README.md             This file
  └── LICENSE               MIT License
```

### Engine Architecture

  ┌──────────┐     create_engine()     ┌───────────────┐
  │   GUI    │ ──────────────────────▶ │   BaseEngine   │
  │  PyQt5   │                         │   (QThread)    │
  └──────────┘                         └───────┬───────┘
                                              │
                    ╭─────────────────────────┼─────────────────────────╮
                    │                         │                         │
              ┌─────▼──────┐          ┌───────▼────────┐
              │  Windows   │          │    Linux       │
              │  WinDivert │          │  NFQUEUE+scapy │
              │  pydivert  │          │  + iptables    │
              └────────────┘          └────────────────┘
                Windows only             Linux only

### Linux Packet Flow

  ┌─────────┐     ┌──────────┐     ┌────────────┐     ┌──────────┐
  │ Network │────▶│ iptables │────▶│ NFQUEUE    │────▶│ Python   │
  │  Stack  │     │  NFQUEUE │     │  Queue #0  │     │ Callback │
  └─────────┘     └──────────┘     └────────────┘     └────┬─────┘
                                                           │
                                              ┌────────────┴────────────┐
                                              │                         │
                                         ┌────▼────┐             ┌─────▼────┐
                                         │  ACCEPT │             │   DROP   │
                                         │ (allow) │             │ (block)  │
                                         └─────────┘             └──────────┘


## CONFIGURATION

  Settings in engine_linux.py / engine_windows.py:

  • DDoS thresholds:     10000 (1s) / 50000 (10s)
  • Blacklist duration:  60 seconds
  • Whitelist:           127.0.0.1, ::1

  Styling in styles.py:
  • Dark theme colors, fonts, padding


## ⚠️ IMPORTANT NOTES

  • Linux: MUST run as root (sudo) — iptables NFQUEUE requires it.
  • Windows: MUST run as Administrator — WinDivert requires it.
  • Linux uses --queue-bypass: if the app crashes, traffic continues.
  • DNS resolution has a 2-second timeout (configurable).
  • All events are logged to firewall_logs.txt.


## LICENSE

  MIT License — see LICENSE file for details.
  Copyright (c) 2025 ERKAN RISNGITS

