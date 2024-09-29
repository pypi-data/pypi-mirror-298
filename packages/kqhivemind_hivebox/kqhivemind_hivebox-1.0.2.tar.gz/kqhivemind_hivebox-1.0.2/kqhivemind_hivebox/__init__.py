"""
HiveMind NFC reader client for HiveBox
"""
from . import gpio, lcddriver
from .__version__ import __version__

if __name__ == "__main__":
    from .__main__ import main
