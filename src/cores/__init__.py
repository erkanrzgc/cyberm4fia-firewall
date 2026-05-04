import sys as _sys

from .base import BaseEngine


def create_engine(rules, website_filter, parent=None):
    if _sys.platform == "win32":
        from .windows import WindowsEngine
        return WindowsEngine(rules, website_filter, parent)
    else:
        from .linux import LinuxEngine
        return LinuxEngine(rules, website_filter, parent)
