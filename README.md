#anti-cheat
---

# Security Check Script

This script performs security checks on a PC, searching for known cheat processes, cheat files, DS4Windows/DS4, macros, and connected USB devices. It then sends an email notification with the results.

## Prerequisites

### 1. Install Python
1. Download Python from [python.org](https://www.python.org/downloads/).
2. Run the installer and follow the instructions. Ensure you check the option to "Add Python to PATH" during installation.

### 2. Install Required Python Modules
Open Command Prompt and run the following commands to install necessary Python modules:
```bash
pip install psutil pywin32 pyudev
```

### 3. Update Email Configuration
Open the script (`security_check.py`) in a text editor and update the following lines with your email details:
```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Use an App Password if 2-Step Verification is enabled
TO_EMAIL_ADDRESS = "recipient_email@gmail.com"
```
- Replace `your_email@gmail.com` with your Gmail address.
- Replace `your_app_password` with your Gmail App Password (recommended if you have 2-Step Verification enabled).
- Replace `recipient_email@gmail.com` with the email address where you want to receive notifications.

## Running the Script on Windows

### 4. Open Command Prompt
1. Press `Win + R`, type `cmd`, and press Enter to open Command Prompt.

### 5. Navigate to Script Directory
Use the `cd` command to navigate to the directory where your script is located:
```cmd
cd path\to\script\directory
```
Replace `path\to\script\directory` with the actual path to the directory containing your script.

### 6. Run the Script
Execute the script by typing:
```cmd
python security_check.py
```
This will start the script execution.

## Monitoring the Output

### 7. Check Command Prompt Output
The script will output messages in the Command Prompt window indicating its progress and findings:
- Checking for suspicious cheat files...
- Checking for known cheat processes...
- Checking for DS4Windows and DS4...
- Checking for macro yy...
- Checking for connected USB devices...

### 8. Email Notification
If the script detects any suspicious activities, it will send an email to the specified `TO_EMAIL_ADDRESS`. Look for a message indicating "Email sent successfully."

## Ending the Test

### 9. Close Command Prompt
Once you've reviewed the script output, you can close the Command Prompt window by typing `exit` and pressing Enter, or clicking the close button on the window.

### 10. Review Results
Check the Command Prompt output for any suspicious activities detected by the script. Also, check your email inbox for the notification email if the script found any issues.

### 11. Modify and Rerun (if needed)
If you need to modify the script or its configuration (e.g., add more checks, change email settings), edit the script accordingly and rerun it using the steps above.

---

## Detailed Script Explanation

The script performs the following checks:

1. **Get Current User**: Retrieves the username of the current user.
2. **Check Suspicious Files**: Searches common directories for files with known cheat or anti-recoil names/extensions.
3. **Check Known Cheat Processes**: Uses `psutil` to check running processes against a list of known cheat processes.
4. **Check USB Devices**: Lists connected USB devices (works across all platforms).
5. **Send Email**: Sends an email with the results of the checks.

## Example Output

```plaintext
Current User: your_username

Checking for suspicious cheat files...
No suspicious cheat files found.

Checking for known cheat processes...
No known cheat processes found.

Checking for connected USB devices...
No connected USB devices found.

Email sent successfully.
```

## Notes for Other Platforms

### macOS and Linux
The script is designed to work on macOS and Linux with the following considerations:
- **macOS**: Uses `system_profiler` to check USB devices.
- **Linux**: Uses `pyudev` to check USB devices.
- Install the required modules using `pip install psutil pyudev`.
