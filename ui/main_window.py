"""
main_window.py - Main application window for VPN Manager.

Provides the PyQt6 GUI with:
- VPN connection list (left panel)
- Control buttons (right panel)
- Import WireGuard / Add L2TP/PPTP dialogs
"""

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QDialog, QFormLayout,
    QLineEdit, QComboBox, QHeaderView
)
from PyQt6.QtCore import Qt

from vpn_gui.core.vpn_manager import VPNManager


class AddVPNDialog(QDialog):
    """Dialog for adding L2TP or PPTP VPN connections."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add L2TP / PPTP Connection")
        self.setMinimumWidth(400)

        layout = QFormLayout()

        # Connection name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., My VPN")
        layout.addRow("Name:", self.name_input)

        # Server address
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("e.g., vpn.example.com")
        layout.addRow("Server:", self.server_input)

        # Username
        self.username_input = QLineEdit()
        layout.addRow("Username:", self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Password:", self.password_input)

        # VPN Type selector
        self.type_combo = QComboBox()
        self.type_combo.addItems(["L2TP", "PPTP"])
        layout.addRow("Type:", self.type_combo)

        # Buttons
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Create")
        self.cancel_btn = QPushButton("Cancel")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addRow(btn_layout)

        self.setLayout(layout)

    def get_values(self):
        """Return the form values as a dict."""
        return {
            "name": self.name_input.text().strip(),
            "server": self.server_input.text().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text().strip(),
            "type": self.type_combo.currentText()
        }


class MainWindow(QMainWindow):
    """Main application window for VPN Manager."""

    def __init__(self):
        super().__init__()
        self.vpn_manager = VPNManager()
        self._init_ui()
        self.refresh_list()

    def _init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("VPN Manager")
        self.setMinimumSize(700, 450)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Main layout
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        # Title
        title = QLabel("VPN Manager")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title)

        # Content area (left: table, right: buttons)
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # --- Left panel: Connection table ---
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Status"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Stretch columns to fill available space
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        content_layout.addWidget(self.table, stretch=3)

        # --- Right panel: Buttons ---
        btn_layout = QVBoxLayout()
        content_layout.addLayout(btn_layout, stretch=1)

        # Connect button
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self._on_connect)
        btn_layout.addWidget(self.connect_btn)

        # Disconnect button
        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self._on_disconnect)
        btn_layout.addWidget(self.disconnect_btn)

        # Separator
        btn_layout.addSpacing(20)

        # Import WireGuard button
        self.import_wg_btn = QPushButton("Import WireGuard")
        self.import_wg_btn.clicked.connect(self._on_import_wireguard)
        btn_layout.addWidget(self.import_wg_btn)

        # Add L2TP/PPTP button
        self.add_vpn_btn = QPushButton("Add L2TP / PPTP")
        self.add_vpn_btn.clicked.connect(self._on_add_vpn)
        btn_layout.addWidget(self.add_vpn_btn)

        # Separator
        btn_layout.addSpacing(20)

        # Refresh button
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_list)
        btn_layout.addWidget(self.refresh_btn)

        # Push buttons to top
        btn_layout.addStretch()

        # Status bar
        self.statusBar().showMessage("Ready")

    def refresh_list(self):
        """Refresh the VPN connection list."""
        self.statusBar().showMessage("Refreshing...")

        connections = self.vpn_manager.get_all_connections()

        self.table.setRowCount(0)
        for conn in connections:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(conn["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(conn["type"]))

            # Color-coded status
            status_item = QTableWidgetItem(conn["status"])
            if conn["status"] == "Connected":
                status_item.setForeground(Qt.GlobalColor.green)
            else:
                status_item.setForeground(Qt.GlobalColor.red)
            self.table.setItem(row, 2, status_item)

        count = len(connections)
        self.statusBar().showMessage(f"Found {count} connection(s)")

    def _get_selected_connection(self):
        """Get the currently selected connection from the table."""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection",
                                "Please select a connection first.")
            return None, None

        row = selected[0].row()
        name = self.table.item(row, 0).text()
        vpn_type = self.table.item(row, 1).text()
        return name, vpn_type

    def _on_connect(self):
        """Handle Connect button click."""
        name, vpn_type = self._get_selected_connection()
        if name is None:
            return

        self.statusBar().showMessage(f"Connecting to {name}...")
        error = self.vpn_manager.connect(name, vpn_type)

        if error:
            QMessageBox.critical(self, "Connection Error",
                                 f"Failed to connect to {name}:\n{error}")
        else:
            QMessageBox.information(self, "Connected",
                                    f"Successfully connected to {name}")

        self.refresh_list()

    def _on_disconnect(self):
        """Handle Disconnect button click."""
        name, vpn_type = self._get_selected_connection()
        if name is None:
            return

        self.statusBar().showMessage(f"Disconnecting {name}...")
        error = self.vpn_manager.disconnect(name, vpn_type)

        if error:
            QMessageBox.critical(self, "Disconnection Error",
                                 f"Failed to disconnect {name}:\n{error}")
        else:
            QMessageBox.information(self, "Disconnected",
                                    f"Successfully disconnected from {name}")

        self.refresh_list()

    def _on_import_wireguard(self):
        """Handle Import WireGuard button click."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select WireGuard Configuration",
            "",
            "WireGuard Config (*.conf);;All Files (*)"
        )

        if not file_path:
            return  # User cancelled

        self.statusBar().showMessage(f"Importing {file_path}...")
        error = self.vpn_manager.import_wireguard(file_path)

        if error:
            QMessageBox.critical(self, "Import Error",
                                 f"Failed to import config:\n{error}")
        else:
            QMessageBox.information(self, "Import Successful",
                                    "WireGuard configuration imported successfully.")

        self.refresh_list()

    def _on_add_vpn(self):
        """Handle Add L2TP/PPTP button click."""
        dialog = AddVPNDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return  # User cancelled

        values = dialog.get_values()

        # Validate form inputs
        if not all([values["name"], values["server"],
                    values["username"], values["password"]]):
            QMessageBox.warning(self, "Incomplete Form",
                                "Please fill in all fields.")
            return

        self.statusBar().showMessage(f"Creating {values['type']} connection...")

        if values["type"] == "L2TP":
            error = self.vpn_manager.create_l2tp(
                values["name"], values["server"],
                values["username"], values["password"]
            )
        else:
            error = self.vpn_manager.create_pptp(
                values["name"], values["server"],
                values["username"], values["password"]
            )

        if error:
            QMessageBox.critical(self, "Creation Error",
                                 f"Failed to create connection:\n{error}")
        else:
            QMessageBox.information(self, "Connection Created",
                                    f"{values['type']} connection '{values['name']}' created.")

        self.refresh_list()
