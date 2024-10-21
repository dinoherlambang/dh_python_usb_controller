# DH Python USB Controller

DH Python USB Controller is a simple system tray application that allows users to enable or disable USB storage devices on Windows systems. It provides a convenient way to control USB access without diving into the Windows Registry manually.

## Features

- Enable USB storage devices
- Disable USB storage devices
- System tray integration for easy usage

## Requirements

- Windows operating system
- Python 3.6+
- PyQt5

## Installation

1. Clone this repository or download the `dh_usb_controller.py` file.

2. Install the required dependencies:

```bash
pip install PyQt5
```

3. Run the script with administrator privileges:
```bash
python dh_usb_controller.py
```

## Creating an Executable (.exe)

To create a standalone executable for easier distribution and use, follow these steps:

1. Install PyInstaller:

```bash
pip install pyinstaller
```
2. Navigate to the directory containing dh_usb_controller.py in your terminal
3. Run PyInstaller with the following command:

```bash
pyinstaller --onefile --windowed --icon=path_to_your_icon.ico dh_usb_controller.py
```
Replace path_to_your_icon.ico with the path to an .ico file if you want to use a custom icon. If you don't have an icon, you can omit the --icon option.

4. Once the process completes, you'll find the executable in the dist folder within your project directory.
5. You can now distribute this .exe file to run the USB Controller on Windows systems without requiring Python installation.

Note: When running the .exe, users may still need to grant administrator privileges for the application to modify registry settings

## Usage
1. After running the script, you'll see a new icon in your system tray.
2. Right-click on the icon to open the menu.
3. Choose from the following options:
    "Enable USB": Enables USB storage devices
    "Disable USB": Disables USB storage devices
    "Exit": Closes the application
4. After selecting "Enable USB" or "Disable USB", you'll see a confirmation message.
5. You may need to restart your computer for the changes to take effect.

## How it Works
The application modifies the Windows Registry to control USB storage devices. Specifically, it changes the 'Start' value in the HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\USBSTOR key:

    - Setting the value to 3 enables USB storage devices
    - Setting the value to 4 disables USB storage devices

Important Notes
    - This application requires administrator privileges to modify the Windows Registry.
    - Use this tool responsibly. Disabling USB storage can impact system functionality.
    - Always ensure you have alternative ways to access your system in case of issues.

