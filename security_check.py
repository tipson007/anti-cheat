import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import platform
import psutil
import sys

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "terraformaft@gmail.com"
EMAIL_PASSWORD = 'rgok qhmz kycz opvx'
TO_EMAIL_ADDRESS = "codcdl1@gmail.com"

known_cheat_processes = [
    "cronus.dll",              # Windows
    "aimbot.dll",              # Windows
    "wallhack.dll",            # Windows
    "macro.dll",               # Windows
    "aimassist.dll",           # Windows
    "cronus.dylib",            # macOS
    "aimbot.dylib",            # macOS
    "wallhack.dylib",          # macOS
    "macro.dylib",             # macOS
    "aimassist.dylib",         # macOS
    "cronus.so",               # Linux
    "aimbot.so",               # Linux
    "wallhack.so",             # Linux
    "macro.so",                # Linux
    "aimassist.so",            # Linux
    "cronus.cpg",              # Cronus Zen
    "ds4windows.exe",          # DS4Windows
    "ds4.exe",                 # DS4
]

known_cheat_files = [
    "anti-recoil.exe",         # Windows
    "recoil-helper.exe",       # Windows
    "anti-recoil",             # macOS/Linux
]

known_anti_recoil_names = [
    "anti-recoil.exe",         # Windows
    "recoil-helper.exe",       # Windows
    "anti-recoil",             # macOS/Linux
    "ds4windows.exe",          # DS4Windows
    "ds4.exe",                 # DS4
]

def get_current_user():
    return os.getlogin()

def check_suspicious_files():
    suspicious_files = []

    if platform.system() == "Windows":
        common_dirs = ["C:\\Program Files", "C:\\Program Files (x86)", "C:\\Users\\Public"]
    elif platform.system() == "Darwin":  
        common_dirs = ["/Applications", "/Users/Shared"]
    elif platform.system() == "Linux":
        common_dirs = ["/usr/bin", "/usr/local/bin", "/opt"]
    else:
        print(f"Unsupported operating system: {platform.system()}")
        return suspicious_files

    for dir in common_dirs:
        for root, dirs, files in os.walk(dir):
            for file in files:
                if any(file.endswith(ext) or any(name in file.lower() for name in known_cheat_processes) for ext in known_cheat_processes):
                    suspicious_files.append(os.path.join(root, file))

    return suspicious_files

def check_known_cheat_processes():
    suspicious_processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in known_cheat_processes:
            suspicious_processes.append(proc.info)
    return suspicious_processes

def check_usb_devices():
    usb_devices = []
    try:
        if platform.system() == "Windows":
            import pyudev
            context = pyudev.Context()
            for device in context.list_devices(subsystem='usb'):
                usb_devices.append(str(device.device_node))
        
        elif platform.system() == "Darwin":
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
        
        elif platform.system() == "Linux":
            import pyudev
            context = pyudev.Context()
            for device in context.list_devices(subsystem='usb'):
                usb_devices.append(str(device.device_node))
        
    except Exception as e:
        print(f"Error checking USB devices: {e}")
    
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
    usb_devices = check_usb_devices()
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