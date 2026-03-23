# VPN Manager — Documentation

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Module Reference](#module-reference)
3. [System Integration](#system-integration)
4. [Error Handling](#error-handling)
5. [Security Considerations](#security-considerations)
6. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

VPN Manager follows a modular 3-layer architecture:

```
┌─────────────────────────────────┐
│         UI Layer (PyQt6)        │
│       ui/main_window.py         │
├─────────────────────────────────┤
│       Core Layer (Logic)        │
│     core/vpn_manager.py         │
│  ┌──────────┐  ┌──────────────┐ │
│  │wireguard │  │    nmcli     │ │
│  │   .py    │  │     .py      │ │
│  └──────────┘  └──────────────┘ │
├─────────────────────────────────┤
│       Utils Layer (Shell)       │
│        utils/shell.py           │
└─────────────────────────────────┘
```

- **UI Layer** — PyQt6 widgets, user interaction, dialogs
- **Core Layer** — Business logic, VPN type routing
- **Utils Layer** — Low-level subprocess execution

---

## Module Reference

### `utils/shell.py`

| Function | Signature | Description |
|----------|-----------|-------------|
| `run_command` | `(cmd: list) -> Tuple[str, str]` | Execute a system command, returns `(stdout, stderr)`. Includes 30s timeout. |

### `core/wireguard.py`

| Function | Description |
|----------|-------------|
| `list_configs()` | Lists all `.conf` files in `/etc/wireguard/` |
| `connect(name)` | Runs `wg-quick up <name>` |
| `disconnect(name)` | Runs `wg-quick down <name>` |
| `import_config(file_path)` | Copies `.conf` to `/etc/wireguard/` with `0600` permissions |

### `core/nmcli.py`

| Function | Description |
|----------|-------------|
| `list_connections()` | Lists all VPN connections via `nmcli` |
| `list_active()` | Lists only active VPN connections |
| `connect(name)` | Runs `nmcli connection up <name>` |
| `disconnect(name)` | Runs `nmcli connection down <name>` |
| `create_l2tp(...)` | Creates L2TP connection via `nmcli connection add` |
| `create_pptp(...)` | Creates PPTP connection via `nmcli connection add` |

### `core/vpn_manager.py`

| Method | Description |
|--------|-------------|
| `get_all_connections()` | Merges WireGuard + NetworkManager connections |
| `connect(name, type)` | Routes to correct backend based on type |
| `disconnect(name, type)` | Routes to correct backend based on type |
| `import_wireguard(path)` | Delegates to `wireguard.import_config()` |
| `create_l2tp(...)` | Delegates to `nmcli.create_l2tp()` |
| `create_pptp(...)` | Delegates to `nmcli.create_pptp()` |

### `ui/main_window.py`

| Class | Description |
|-------|-------------|
| `MainWindow` | Main application window with table and control buttons |
| `AddVPNDialog` | Modal dialog for creating L2TP/PPTP connections |

---

## System Integration

### WireGuard

- **Config directory:** `/etc/wireguard/`
- **Commands used:** `wg-quick up/down`, `ip link show`
- **Required packages:** `wireguard`, `wireguard-tools`

### L2TP

- **Managed by:** NetworkManager
- **Commands used:** `nmcli connection add/up/down`
- **Required packages:** `network-manager-l2tp`

### PPTP

- **Managed by:** NetworkManager
- **Commands used:** `nmcli connection add/up/down`
- **Required packages:** `network-manager-pptp`

---

## Error Handling

All operations show error dialogs on failure:

| Scenario | Handling |
|----------|----------|
| **Command failure** | Error message box with stderr output |
| **Invalid config file** | Validation before import; rejection message |
| **Permission denied** | Warning dialog + suggestion to run as root |
| **Command not found** | Caught by `shell.py`, displayed in UI |
| **Timeout** | 30-second limit per command; timeout error shown |

---

## Security Considerations

- **Root access:** Required for WireGuard and NetworkManager operations
- **pkexec:** Used for privilege escalation when not running as root
- **Config permissions:** Imported WireGuard configs set to `0600` (root-only)
- **Passwords:** Stored via NetworkManager's built-in secret storage

---

## Troubleshooting

### App won't start

```bash
# Check Python version
python3 --version  # Must be 3.8+

# Check PyQt6 is installed
pip show PyQt6

# Check system packages
which wg-quick
which nmcli
```

### WireGuard connections not showing

```bash
# Check if config directory exists
ls -la /etc/wireguard/

# Verify permissions
sudo ls -la /etc/wireguard/
```

### L2TP/PPTP creation fails

```bash
# Check NetworkManager plugins
nmcli general
sudo apt install network-manager-l2tp network-manager-pptp

# Restart NetworkManager
sudo systemctl restart NetworkManager
```

### Permission errors

```bash
# Run with sudo
sudo python3 -m vpn_gui.main

# Or ensure pkexec works
pkexec --help
```
