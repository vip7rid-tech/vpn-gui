"""
nmcli.py - NetworkManager CLI integration module.

Handles L2TP and PPTP VPN connections through nmcli,
including creating, listing, connecting, and disconnecting.
"""

from typing import List, Dict

from vpn_gui.utils.shell import run_command


def list_connections() -> List[Dict[str, str]]:
    """
    List all VPN connections managed by NetworkManager.

    Returns:
        List of dicts with keys: 'name', 'type', 'status'
    """
    stdout, stderr = run_command([
        "nmcli", "-t", "-f", "NAME,TYPE,ACTIVE",
        "connection", "show"
    ])

    if stderr or not stdout:
        return []

    connections = []
    active_names = _get_active_names()

    for line in stdout.splitlines():
        parts = line.split(":")
        if len(parts) >= 3:
            name = parts[0]
            conn_type = parts[1]

            # Filter to only VPN-related connection types
            if _is_vpn_type(conn_type):
                status = "Connected" if name in active_names else "Disconnected"
                display_type = _format_type(conn_type)
                connections.append({
                    "name": name,
                    "type": display_type,
                    "status": status
                })

    return connections


def _get_active_names() -> List[str]:
    """
    Get names of all currently active connections.

    Returns:
        List of active connection names
    """
    stdout, _ = run_command([
        "nmcli", "-t", "-f", "NAME",
        "connection", "show", "--active"
    ])
    if not stdout:
        return []
    return [line.strip() for line in stdout.splitlines() if line.strip()]


def list_active() -> List[Dict[str, str]]:
    """
    List only currently active VPN connections.

    Returns:
        List of dicts with keys: 'name', 'type'
    """
    stdout, _ = run_command([
        "nmcli", "-t", "-f", "NAME,TYPE",
        "connection", "show", "--active"
    ])

    if not stdout:
        return []

    active = []
    for line in stdout.splitlines():
        parts = line.split(":")
        if len(parts) >= 2 and _is_vpn_type(parts[1]):
            active.append({
                "name": parts[0],
                "type": _format_type(parts[1])
            })

    return active


def connect(name: str) -> str:
    """
    Activate a VPN connection.

    Args:
        name: Connection name as shown in nmcli

    Returns:
        Empty string on success, error message on failure
    """
    stdout, stderr = run_command(["nmcli", "connection", "up", name])
    if stderr:
        return stderr
    return ""


def disconnect(name: str) -> str:
    """
    Deactivate a VPN connection.

    Args:
        name: Connection name as shown in nmcli

    Returns:
        Empty string on success, error message on failure
    """
    stdout, stderr = run_command(["nmcli", "connection", "down", name])
    if stderr:
        return stderr
    return ""


def create_l2tp(name: str, server: str, username: str, password: str) -> str:
    """
    Create a new L2TP VPN connection via nmcli.

    Args:
        name: Connection name
        server: VPN server address
        username: Authentication username
        password: Authentication password

    Returns:
        Empty string on success, error message on failure
    """
    # Create the L2TP connection
    stdout, stderr = run_command([
        "nmcli", "connection", "add",
        "type", "vpn",
        "con-name", name,
        "vpn-type", "l2tp",
        "ifname", "--",
        "vpn.data",
        f"gateway={server},user={username},password-flags=0",
        "vpn.secrets",
        f"password={password}"
    ])

    if stderr and "error" in stderr.lower():
        return stderr
    return ""


def create_pptp(name: str, server: str, username: str, password: str) -> str:
    """
    Create a new PPTP VPN connection via nmcli.

    Args:
        name: Connection name
        server: VPN server address
        username: Authentication username
        password: Authentication password

    Returns:
        Empty string on success, error message on failure
    """
    # Create the PPTP connection
    stdout, stderr = run_command([
        "nmcli", "connection", "add",
        "type", "vpn",
        "con-name", name,
        "vpn-type", "pptp",
        "ifname", "--",
        "vpn.data",
        f"gateway={server},user={username},password-flags=0",
        "vpn.secrets",
        f"password={password}"
    ])

    if stderr and "error" in stderr.lower():
        return stderr
    return ""


def _is_vpn_type(conn_type: str) -> bool:
    """Check if a connection type string represents a VPN."""
    vpn_keywords = ["vpn", "wireguard", "l2tp", "pptp"]
    return any(kw in conn_type.lower() for kw in vpn_keywords)


def _format_type(conn_type: str) -> str:
    """Format the connection type for display."""
    lower = conn_type.lower()
    if "l2tp" in lower:
        return "L2TP"
    elif "pptp" in lower:
        return "PPTP"
    elif "wireguard" in lower:
        return "WireGuard"
    elif "vpn" in lower:
        return "VPN"
    return conn_type
