# VPN Manager

A minimal, functional Linux desktop GUI application for managing VPN connections.  
Supports **WireGuard**, **L2TP**, and **PPTP** protocols.

---

## Features

- **Import WireGuard** — Import `.conf` files directly to `/etc/wireguard/`
- **Add L2TP / PPTP** — Create connections via NetworkManager (nmcli)
- **Connect / Disconnect** — One-click VPN toggling
- **Status Detection** — Live connection status display
- **Root Privilege Handling** — Auto-escalation via `pkexec`

---

## Requirements

### System

- **OS:** Linux (tested on Ubuntu/Debian)
- **Python:** 3.8+
- **WireGuard tools:** `wg`, `wg-quick`
- **NetworkManager:** `nmcli`
- **PolicyKit:** `pkexec` (optional, for privilege escalation)

### System Packages (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y wireguard network-manager \
    network-manager-l2tp network-manager-pptp \
    python3 python3-pip python3-venv
```

---

## Installation

```bash
# Clone or copy the project
cd vpn-manager

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

---

## Usage

### Run the application

```bash
# Run as root (recommended)
sudo venv/bin/python -m vpn_gui.main

# Or without root (will attempt pkexec escalation)
python -m vpn_gui.main
```

### GUI Overview

| Area | Description |
|------|-------------|
| **Left Panel** | List of all VPN connections with name, type, and status |
| **Connect** | Activate the selected VPN connection |
| **Disconnect** | Deactivate the selected VPN connection |
| **Import WireGuard** | Import a `.conf` file |
| **Add L2TP / PPTP** | Open form to create a new connection |
| **Refresh** | Reload the connection list |

---

## Project Structure
  
```
vpn_gui/
├── main.py              # Entry point, root check
├── __init__.py
├── ui/
│   ├── __init__.py
│   └── main_window.py   # PyQt6 GUI
├── core/
│   ├── __init__.py
│   ├── vpn_manager.py   # Unified VPN interface
│   ├── wireguard.py     # WireGuard backend
│   └── nmcli.py         # NetworkManager backend
└── utils/
    ├── __init__.py
    └── shell.py          # Subprocess wrapper
```

---

## License

This project is provided as-is for personal use.
