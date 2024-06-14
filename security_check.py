
import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import platform
import psutil
import sys
import win32com.client

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "terraformaft@gmail.com"
EMAIL_PASSWORD = 'rgok qhmz kycz opvx'
TO_EMAIL_ADDRESS = "codcdl1@gmail.com"

known_cheat_processes = [
    "cronus.dll", "aimbot.dll", "wallhack.dll", "macro.dll", "aimassist.dll",
    "cronus.dylib", "aimbot.dylib", "wallhack.dylib", "macro.dylib", "aimassist.dylib",
    "cronus.so", "aimbot.so", "wallhack.so", "macro.so", "aimassist.so",
    "cronus.cpg", "ds4windows.exe", "ds4.exe"
]

known_cheat_files = [
    "anti-recoil.exe", "recoil-helper.exe", "anti-recoil",
    "ds4windows.exe", "ds4.exe"
]

known_cheat_extensions = [
    ".dylib", ".cpg"
]

def get_current_user():
    return os.getlogin()

def check_suspicious_files():
    suspicious_files = []

    if platform.system() == "Windows":
        common_dirs = ["C:\\Program Files", "C:\\Program Files (x86)", "C:\\Users\\Public", "C:\\"]
    elif platform.system() == "Darwin":
        common_dirs = ["/Applications", "/Users/Shared", "/"]
    elif platform.system() == "Linux":
        common_dirs = ["/usr/bin", "/usr/local/bin", "/opt", "/"]
    else:
        print(f"Unsupported operating system: {platform.system()}")
        return suspicious_files

    for dir in common_dirs:
        for root, dirs, files in os.walk(dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in known_cheat_extensions) or any(name in file.lower() for name in known_cheat_files):
                    suspicious_files.append(os.path.join(root, file))

    return suspicious_files

def check_known_cheat_processes():
    suspicious_processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in known_cheat_processes:
            suspicious_processes.append(proc.info)
    return suspicious_processes

def check_usb_devices_windows():
    usb_devices = []
    try:
        cmd = 'Get-WmiObject Win32_USBHub | Select-Object DeviceID, Description, Manufacturer, Status, PNPDeviceID'
        result = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True)
        devices = result.stdout.strip().split('\n\n')
        for device in devices:
            device_info = {}
            for line in device.split('\n'):
                if ':' in line:
                    key, value = map(str.strip, line.split(':', 1))
                    device_info[key] = value
            if device_info:
                device_details = (
                    f"Description: {device_info.get('Description', 'N/A')}\n"
                    f"Manufacturer: {device_info.get('Manufacturer', 'N/A')}\n"
                    f"Device ID: {device_info.get('DeviceID', 'N/A')}\n"
                    f"Status: {device_info.get('Status', 'N/A')}\n"
                    f"PNP Device ID: {device_info.get('PNPDeviceID', 'N/A')}\n"
                )
                usb_devices.append(device_details)
    except Exception as e:
        print(f"Error checking USB devices on Windows: {e}")
    return usb_devices
    
def check_usb_devices_macos():
    usb_devices = []
    try:
        result = subprocess.run(['system_profiler', 'SPUSBDataType'], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith("Location ID:"):
                usb_device_info = line
                while i + 1 < len(lines) and not lines[i + 1].strip().startswith("Location ID:"):
                    i += 1
                    usb_device_info += "\n" + lines[i].strip()
                usb_devices.append(usb_device_info)
    except Exception as e:
        print(f"Error checking USB devices on macOS: {e}")
    return usb_devices

def check_usb_devices_linux():
    usb_devices = []
    try:
        import pyudev
        context = pyudev.Context()
        for device in context.list_devices(subsystem='usb'):
            usb_devices.append(str(device.device_node))
    except Exception as e:
        print(f"Error checking USB devices on Linux: {e}")
    return usb_devices

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL_ADDRESS
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL_ADDRESS, text)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    results = []

    current_user = get_current_user()
    results.append(f"Current User: {current_user}\n")

    print("Checking for suspicious cheat files...")
    files = check_suspicious_files()
    if files:
        results.append("Suspicious cheat files found:")
        for file in files:
            results.append(file)
    else:
        results.append("No suspicious cheat files found.")

    print("\nChecking for known cheat processes...")
    processes = check_known_cheat_processes()
    if processes:
        results.append("Known cheat processes found:")
        for proc in processes:
            results.append(f"Process ID: {proc['pid']}, Name: {proc['name']}")
    else:
        results.append("No known cheat processes found.")

    print("\nChecking for connected USB devices...")
    if platform.system() == "Windows":
        usb_devices = check_usb_devices_windows()
    elif platform.system() == "Darwin":
        usb_devices = check_usb_devices_macos()
    elif platform.system() == "Linux":
        usb_devices = check_usb_devices_linux()
    else:
        usb_devices = []

    if usb_devices:
        results.append("\nConnected USB devices found:")
        for device in usb_devices:
            results.append(device)
    else:
        results.append("\nNo connected USB devices found.")

    subject = "Security Check Completed"
    body = "\n".join(results)
    print(body)
    send_email(subject, body)

if __name__ == "__main__":
    main()
