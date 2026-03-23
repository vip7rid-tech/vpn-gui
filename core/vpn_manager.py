"""
vpn_manager.py - Unified VPN management interface.

Provides a single entry point for managing all VPN types
(WireGuard, L2TP, PPTP) by routing commands to the
appropriate backend module.
"""

from typing import List, Dict

from vpn_gui.core import wireguard, nmcli


class VPNManager:
    """
    Unified manager for all VPN connection types.
    Routes operations to WireGuard or NetworkManager backends
    based on the connection type.
    """

    def get_all_connections(self) -> List[Dict[str, str]]:
        """
        Get a combined list of all VPN connections.

        Returns:
            List of dicts with keys: 'name', 'type', 'status'
        """
        connections = []

        # Get WireGuard connections
        try:
            wg_conns = wireguard.list_configs()
            connections.extend(wg_conns)
        except Exception:
            pass  # WireGuard may not be installed

        # Get NetworkManager VPN connections
        try:
            nm_conns = nmcli.list_connections()
            connections.extend(nm_conns)
        except Exception:
            pass  # nmcli may not be available

        return connections

    def connect(self, name: str, vpn_type: str) -> str:
        """
        Connect to a VPN by name and type.

        Args:
            name: Connection name
            vpn_type: Type of VPN ('WireGuard', 'L2TP', 'PPTP', 'VPN')

        Returns:
            Empty string on success, error message on failure
        """
        if vpn_type == "WireGuard":
            return wireguard.connect(name)
        else:
            return nmcli.connect(name)

    def disconnect(self, name: str, vpn_type: str) -> str:
        """
        Disconnect a VPN by name and type.

        Args:
            name: Connection name
            vpn_type: Type of VPN ('WireGuard', 'L2TP', 'PPTP', 'VPN')

        Returns:
            Empty string on success, error message on failure
        """
        if vpn_type == "WireGuard":
            return wireguard.disconnect(name)
        else:
            return nmcli.disconnect(name)

    def import_wireguard(self, file_path: str) -> str:
        """
        Import a WireGuard configuration file.

        Args:
            file_path: Path to the .conf file

        Returns:
            Empty string on success, error message on failure
        """
        return wireguard.import_config(file_path)

    def create_l2tp(self, name: str, server: str,
                    username: str, password: str) -> str:
        """
        Create a new L2TP VPN connection.

        Returns:
            Empty string on success, error message on failure
        """
        return nmcli.create_l2tp(name, server, username, password)

    def create_pptp(self, name: str, server: str,
                    username: str, password: str) -> str:
        """
        Create a new PPTP VPN connection.

        Returns:
            Empty string on success, error message on failure
        """
        return nmcli.create_pptp(name, server, username, password)
