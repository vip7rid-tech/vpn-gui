#!/usr/bin/env python3
"""
main.py - Entry point for VPN Manager application.

Checks for root permissions and launches the PyQt6 GUI.
If not running as root, attempts to re-launch with pkexec.
"""

import os
import sys
import subprocess


def check_root():
    """
    Check if the application is running with root privileges.
    If not, attempt to restart with pkexec or show a warning.
    """
    if os.geteuid() != 0:
        print("Warning: VPN Manager requires root privileges.")
        print("Attempting to restart with pkexec...")

        try:
            # Re-launch the application with pkexec for root access
            subprocess.Popen(
                ["pkexec", sys.executable] + sys.argv
            )
            sys.exit(0)
        except FileNotFoundError:
            print("pkexec not found. Please run as root:")
            print(f"  sudo {sys.executable} {' '.join(sys.argv)}")
            # Continue anyway - some features may not work
            return False

    return True


def main():
    """Main entry point."""
    # Check root privileges
    is_root = check_root()

    # Import PyQt6 after root check (avoid importing if we're restarting)
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from vpn_gui.ui.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setApplicationName("VPN Manager")

    window = MainWindow()

    # Show warning if not running as root
    if not is_root:
        QMessageBox.warning(
            window,
            "Permission Warning",
            "VPN Manager is not running as root.\n"
            "Some features may not work correctly.\n\n"
            "Please restart with: sudo python3 main.py"
        )

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
