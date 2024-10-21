import sys
import os
import winreg
from PyQt5 import QtWidgets, QtGui

class USBControllerApp(QtWidgets.QSystemTrayIcon):
    def __init__(self):
        super(USBControllerApp, self).__init__()

        # Set up tray icon
        self.setIcon(QtGui.QIcon(QtGui.QPixmap(16, 16)))
        self.setToolTip("USB Controller")

        # Create the menu for the system tray
        self.menu = QtWidgets.QMenu()

        # Add options to enable, disable USB, and exit
        enable_action = self.menu.addAction("Enable USB")
        disable_action = self.menu.addAction("Disable USB")
        
        # Add startup toggle option
        self.startup_action = self.menu.addAction("Run at Startup")
        self.startup_action.setCheckable(True)
        self.startup_action.setChecked(self.is_startup_enabled())
        
        exit_action = self.menu.addAction("Exit")

        # Connect the actions to methods
        enable_action.triggered.connect(self.enable_usb)
        disable_action.triggered.connect(self.disable_usb)
        self.startup_action.triggered.connect(self.toggle_startup)
        exit_action.triggered.connect(self.exit_app)

        # Set the menu to the system tray icon
        self.setContextMenu(self.menu)
        self.show()

    def modify_usb_registry(self, enable=True):
        try:
            # Open the registry key for USBSTOR
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Services\USBSTOR', 0, winreg.KEY_SET_VALUE)

            # Set the value to 3 (enable) or 4 (disable)
            if enable:
                winreg.SetValueEx(key, 'Start', 0, winreg.REG_DWORD, 3)
            else:
                winreg.SetValueEx(key, 'Start', 0, winreg.REG_DWORD, 4)

            # Close the key
            winreg.CloseKey(key)

            # Show confirmation
            QtWidgets.QMessageBox.information(None, "USB Controller", f"USB devices {'enabled' if enable else 'disabled'} successfully.")

        except Exception as e:
            # Show error if modifying registry fails
            QtWidgets.QMessageBox.critical(None, "USB Controller", f"Failed to modify USB settings: {str(e)}")

    def enable_usb(self):
        self.modify_usb_registry(enable=True)

    def disable_usb(self):
        self.modify_usb_registry(enable=False)

    def is_startup_enabled(self):
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, "DH USB Controller")
            winreg.CloseKey(key)
            return True
        except WindowsError:
            return False

    def toggle_startup(self):
        success = toggle_startup(self.startup_action.isChecked())
        if not success:
            self.startup_action.setChecked(not self.startup_action.isChecked())
            QtWidgets.QMessageBox.warning(None, "Startup Error", "Failed to modify startup settings.")

    def exit_app(self):
        QtWidgets.QApplication.quit()

def toggle_startup(enable):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        if enable:
            executable_path = sys.executable if getattr(sys, 'frozen', False) else __file__
            winreg.SetValueEx(key, "DH USB Controller", 0, winreg.REG_SZ, executable_path)
        else:
            winreg.DeleteValue(key, "DH USB Controller")
        winreg.CloseKey(key)
        return True
    except WindowsError:
        return False

if __name__ == '__main__':
    # Ensure the app has admin privileges (optional)
    app = QtWidgets.QApplication(sys.argv)

    # Create and display the system tray app
    tray_icon = USBControllerApp()
    tray_icon.show()

    # Run the app
    sys.exit(app.exec_())
