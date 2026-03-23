"""
wireguard.py - WireGuard VPN management module.

Handles WireGuard configuration import, connection, disconnection,
and listing via wg-quick and wg CLI tools.
"""

import os
import shutil
from typing import List, Dict

from vpn_gui.utils.shell import run_command

# Default WireGuard configuration directory
WG_CONFIG_DIR = "/etc/wireguard"


def list_configs() -> List[Dict[str, str]]:
    """
    List all WireGuard configurations found in /etc/wireguard/.

    Returns:
        List of dicts with keys: 'name', 'type', 'status'
    """
    configs = []

    # Check if the WireGuard config directory exists
    if not os.path.isdir(WG_CONFIG_DIR):
        return configs

    # Find all .conf files in the WireGuard directory
    for filename in os.listdir(WG_CONFIG_DIR):
        if filename.endswith(".conf"):
            name = filename.replace(".conf", "")
            status = _get_status(name)
            configs.append({
                "name": name,
                "type": "WireGuard",
                "status": status
            })

    return configs


def _get_status(name: str) -> str:
    """
    Check if a WireGuard interface is currently active.

    Args:
        name: WireGuard interface/config name

    Returns:
        'Connected' if the interface is up, 'Disconnected' otherwise
    """
    stdout, _ = run_command(["ip", "link", "show", name])
    if stdout and name in stdout:
        return "Connected"
    return "Disconnected"


def connect(name: str) -> str:
    """
    Bring up a WireGuard connection.

    Args:
        name: Name of the WireGuard config (without .conf extension)

    Returns:
        Empty string on success, error message on failure
    """
    stdout, stderr = run_command(["wg-quick", "up", name])
    if stderr and "already" not in stderr.lower():
        return stderr
    return ""


def disconnect(name: str) -> str:
    """
    Bring down a WireGuard connection.

    Args:
        name: Name of the WireGuard config (without .conf extension)

    Returns:
        Empty string on success, error message on failure
    """
    stdout, stderr = run_command(["wg-quick", "down", name])
    if stderr and "not" not in stderr.lower():
        return stderr
    return ""


def import_config(file_path: str) -> str:
    """
    Import a WireGuard configuration file to /etc/wireguard/.

    Args:
        file_path: Full path to the .conf file to import

    Returns:
        Empty string on success, error message on failure
    """
    # Validate the file exists and has .conf extension
    if not os.path.isfile(file_path):
        return f"File not found: {file_path}"

    if not file_path.endswith(".conf"):
        return "Invalid file: must be a .conf file"

    # Ensure the target directory exists
    if not os.path.isdir(WG_CONFIG_DIR):
        return f"WireGuard config directory not found: {WG_CONFIG_DIR}"

    # Copy the config file to /etc/wireguard/
    try:
        filename = os.path.basename(file_path)
        dest = os.path.join(WG_CONFIG_DIR, filename)
        shutil.copy2(file_path, dest)
        # Set proper permissions (readable only by root)
        os.chmod(dest, 0o600)
        return ""
    except PermissionError:
        return "Permission denied: cannot copy to /etc/wireguard/"
    except Exception as e:
        return f"Failed to import config: {str(e)}"
