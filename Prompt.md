Build a minimal, functional Linux desktop GUI application for managing VPN connections with the following requirements.

## 🎯 MAIN GOAL

Create a simple GUI tool to:

* Import VPN configurations
* Connect / disconnect VPN
* Support:

  * WireGuard
  * L2TP
  * PPTP

UI design is NOT important. Focus on functionality, reliability, and simplicity.

---

## 🧱 TECH STACK

* Language: Python 3
* GUI: PyQt6 (preferred) or PySide6
* System interaction: subprocess (no DBus)
* Target OS: Linux only

---

## ⚙️ SYSTEM INTEGRATION

### Use existing Linux tools:

* WireGuard:

  * wg
  * wg-quick

* NetworkManager (for L2TP & PPTP):

  * nmcli

---

## 🔐 PERMISSIONS

* The app must detect if not run as root
* If not root:

  * Show warning OR
  * Attempt to re-run using pkexec

---

## 📦 FEATURES

### 1. Import Configuration

#### WireGuard:

* Button: "Import WireGuard Config"
* Open file dialog
* Accept .conf file
* Copy file to:
  /etc/wireguard/
* Use filename (without extension) as connection name

#### L2TP / PPTP:

* Simple form input:

  * Name
  * Server
  * Username
  * Password
  * Type (dropdown: L2TP / PPTP)

* Create connection using nmcli

---

### 2. List VPN Connections

* Display list of all VPN connections from:
  nmcli connection show

* Show:

  * Name
  * Type
  * Status (connected / disconnected)

---

### 3. Connect / Disconnect

#### WireGuard:

Use:

* wg-quick up <name>
* wg-quick down <name>

#### Others:

Use:

* nmcli connection up <name>
* nmcli connection down <name>

---

### 4. Status Detection

* Detect active connections using:
  nmcli connection show --active
* Update UI accordingly

---

## 🧩 UI STRUCTURE

Main Window:

* Top: Title "VPN Manager"
* Left: List of connections
* Right:

  * Connect button
  * Disconnect button
  * Import buttons:

    * Import WireGuard
    * Add L2TP/PPTP

No need for fancy UI. Use basic layouts.

---

## 📁 PROJECT STRUCTURE

vpn_gui/

* main.py
* ui/

  * main_window.py
* core/

  * vpn_manager.py
  * wireguard.py
  * nmcli.py
* utils/

  * shell.py

---

## 🧠 IMPLEMENTATION DETAILS

### shell.py

* Wrapper for subprocess:

  * run_command(cmd: list) -> return output, error

---

### wireguard.py

Functions:

* list_configs()
* connect(name)
* disconnect(name)
* import_config(file_path)

---

### nmcli.py

Functions:

* list_connections()
* list_active()
* connect(name)
* disconnect(name)
* create_l2tp(...)
* create_pptp(...)

---

### vpn_manager.py

* Unified interface for all VPN types
* Detect type and route command

---

## ⚠️ ERROR HANDLING

* Show message box on:

  * Command failure
  * Invalid config
  * Permission denied

---

## 🧪 EXTRA REQUIREMENTS

* Code must be clean and modular
* No unnecessary dependencies
* Include comments
* Must be runnable immediately after install

---

## ▶️ RUN INSTRUCTIONS (INCLUDE IN OUTPUT)

Provide steps:

* install dependencies
* run app

---

## 📌 IMPORTANT

* Do NOT overcomplicate
* Do NOT use async unless necessary
* Do NOT use web tech (no Electron, no browser UI)
* Focus on working CLI integration

---

## ✅ FINAL OUTPUT

* Full working code
* All files included
* Ready-to-run Linux VPN GUI app
