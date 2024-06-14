
### Pre-requisites:
1. **Python Installation:**
   - Ensure Python is installed on your Windows PC. You can download Python from [python.org](https://www.python.org/downloads/) and follow the installation instructions.

2. **Required Python Modules:**
   - Install necessary Python modules if they are not already installed:
     ```bash
     pip install psutil pywin32
     ```

3. **Script Configuration:**
   - Update the script with your Gmail credentials (`EMAIL_ADDRESS`, `EMAIL_PASSWORD`, `TO_EMAIL_ADDRESS`) for sending email notifications.

### Execution Steps:

1. **Open a Command Prompt (cmd):**
   - Press `Win + R`, type `cmd`, and press Enter to open Command Prompt.

2. **Navigate to Script Directory:**
   - Use `cd` command to navigate to the directory where your script (`security_check.py`) is located.
     ```cmd
     cd path\to\script\directory
     ```

3. **Run the Script:**
   - Execute the Python script using the following command:
     ```cmd
     python security_check.py
     ```
   - This command will start the script execution.

4. **Monitor Script Output:**
   - The script will output messages to the Command Prompt window indicating its progress and findings:
     - Checking for suspicious cheat files...
     - Checking for known cheat processes...
     - Checking for DS4Windows and DS4...
     - Checking for macro yy...

5. **Email Notification (if configured):**
   - If the script finds any suspicious activities (cheat files, processes, DS4Windows/DS4, macro yy), it will attempt to send an email notification to the specified `TO_EMAIL_ADDRESS`.

6. **Script Completion:**
   - Once the script completes its checks, it will print a summary of its findings in the Command Prompt window.
   - If configured, it will also print "Email sent successfully." indicating that the email notification was sent.

### Ending the Test:

- **Close Command Prompt:** Once you've reviewed the script output, you can close the Command Prompt window by typing `exit` and pressing Enter, or clicking the close button on the window.

- **Review Results:** Check the Command Prompt output for any suspicious activities detected by the script.

- **Modify and Rerun (if needed):** If you want to modify the script or its configuration (e.g., add more checks, change email settings), edit the script accordingly and rerun it using the steps above.

### Note:
- Ensure that your Windows PC is connected to the internet and has Python installed with required modules (`psutil` and `pywin32`).
- Make sure to handle email credentials (`EMAIL_ADDRESS`, `EMAIL_PASSWORD`) securely and in accordance with your email provider's security guidelines (e.g., using App Passwords for Gmail if 2-Step Verification is enabled).

By following these steps, you can effectively run and test the script on a Windows PC to monitor for suspicious activities related to cheat files, processes, and specific applications like DS4Windows and DS4.