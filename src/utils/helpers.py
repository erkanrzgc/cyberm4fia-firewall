import logging
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_FILE = os.path.join(PROJECT_ROOT, "logs", "firewall.log")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_to_file(message, level="info"):
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)


PROTOCOL_MAP = {
    1: "ICMP",
    2: "IGMP",
    6: "TCP",
    8: "EGP",
    9: "IGP",
    17: "UDP",
    41: "IPv6",
    50: "ESP",
    51: "AH",
    58: "ICMPv6",
    89: "OSPF",
    112: "VRRP",
    132: "SCTP",
    137: "MPLS-in-IP",
    143: "EtherIP",
    255: "Experimental"
}


def get_protocol_name(protocol):
    if isinstance(protocol, tuple):
        protocol = protocol[0]
    return PROTOCOL_MAP.get(protocol, f"Unknown ({protocol})")
