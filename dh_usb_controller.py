import sys
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
        exit_action = self.menu.addAction("Exit")

        # Connect the actions to methods
        enable_action.triggered.connect(self.enable_usb)
        disable_action.triggered.connect(self.disable_usb)
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

    def exit_app(self):
        QtWidgets.QApplication.quit()

if __name__ == '__main__':
    # Ensure the app has admin privileges (optional)
    app = QtWidgets.QApplication(sys.argv)

    # Create and display the system tray app
    tray_icon = USBControllerApp()
    tray_icon.show()

    # Run the app
    sys.exit(app.exec_())
