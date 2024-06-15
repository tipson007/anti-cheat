# Email configuration
$SMTPServer = "smtp.gmail.com"
$SMTPPort = 587
$EmailAddress = "terraformaft@gmail.com"
$EmailPassword = "rgok qhmz kycz opvx"
$ToEmailAddress = "codcdl1@gmail.com"

# Known cheat signatures
$knownCheatProcesses = @(
    "cronus.dll", "aimbot.dll", "wallhack.dll", "macro.dll", "aimassist.dll",
    "cronus.dylib", "aimbot.dylib", "wallhack.dylib", "macro.dylib", "aimassist.dylib",
    "cronus.so", "aimbot.so", "wallhack.so", "macro.so", "aimassist.so",
    "cronus.cpg", "ds4windows.exe", "ds4.exe"
)

$knownCheatFiles = @(
    "anti-recoil.exe", "recoil-helper.exe", "anti-recoil",
    "ds4windows.exe", "ds4.exe"
)

$knownCheatExtensions = @(
    ".dylib", ".cpg"
)

# Get current user
function Get-CurrentUser {
    return $env:USERNAME
}

# Check suspicious files
function Check-SuspiciousFiles {
    $suspiciousFiles = @()
    $commonDirs = @()

    if ($IsWindows) {
        $commonDirs = @("C:\Program Files", "C:\Program Files (x86)", "C:\Users\Public", "C:\")
    } elseif ($IsMacOS) {
        $commonDirs = @("/Applications", "/Users/Shared", "/")
    } elseif ($IsLinux) {
        $commonDirs = @("/usr/bin", "/usr/local/bin", "/opt", "/")
    } else {
        Write-Output "Unsupported operating system: $($PSVersionTable.OS)"
        return $suspiciousFiles
    }

    foreach ($dir in $commonDirs) {
        Get-ChildItem -Path $dir -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
            if ($knownCheatExtensions -contains $_.Extension.ToLower() -or
                $knownCheatFiles -contains $_.Name.ToLower()) {
                $suspiciousFiles += $_.FullName
            }
        }
    }

    return $suspiciousFiles
}

# Check known cheat processes
function Check-KnownCheatProcesses {
    $suspiciousProcesses = @()
    Get-Process | ForEach-Object {
        if ($knownCheatProcesses -contains $_.Name) {
            $suspiciousProcesses += @{ pid = $_.Id; name = $_.Name }
        }
    }
    return $suspiciousProcesses
}

# Check USB devices
function Check-USBDevices {
    $usbDevices = @()
    if ($IsWindows) {
        $devices = Get-WmiObject Win32_USBHub | Select-Object DeviceID, Description, Manufacturer, Status, PNPDeviceID
        foreach ($device in $devices) {
            $deviceDetails = "Description: $($device.Description)`nManufacturer: $($device.Manufacturer)`nDevice ID: $($device.DeviceID)`nStatus: $($device.Status)`nPNP Device ID: $($device.PNPDeviceID)"
            $usbDevices += $deviceDetails
        }
    } elseif ($IsMacOS) {
        $result = system_profiler SPUSBDataType
        $devices = $result -split "Location ID:"
        foreach ($device in $devices[1..$devices.Length]) {
            $usbDevices += "Location ID:$device"
        }
    } elseif ($IsLinux) {
        $context = pyudev.Context()
        foreach ($device in $context.ListDevices(subsystem='usb')) {
            $usbDevices += $device.device_node
        }
    }
    return $usbDevices
}

# Send email
function Send-Email {
    param (
        [string]$subject,
        [string]$body
    )

    $msg = New-Object system.net.mail.mailmessage
    $msg.from = $EmailAddress
    $msg.to.add($ToEmailAddress)
    $msg.subject = $subject
    $msg.body = $body

    $smtp = New-Object Net.Mail.SmtpClient($SMTPServer, $SMTPPort)
    $smtp.EnableSsl = $true
    $smtp.Credentials = New-Object System.Net.NetworkCredential($EmailAddress, $EmailPassword)

    try {
        $smtp.Send($msg)
        Write-Output "Email sent successfully."
    } catch {
        Write-Output "Failed to send email: $_"
    }
}

# Main function
function Main {
    $results = @()

    $currentUser = Get-CurrentUser
    $results += "Current User: $currentUser`n"

    Write-Output "Checking for suspicious cheat files..."
    $files = Check-SuspiciousFiles
    if ($files.Count -gt 0) {
        $results += "Suspicious cheat files found:"
        foreach ($file in $files) {
            $results += $file
        }
    } else {
        $results += "No suspicious cheat files found."
    }

    Write-Output "`nChecking for known cheat processes..."
    $processes = Check-KnownCheatProcesses
    if ($processes.Count -gt 0) {
        $results += "Known cheat processes found:"
        foreach ($proc in $processes) {
            $results += "Process ID: $($proc.pid), Name: $($proc.name)"
        }
    } else {
        $results += "No known cheat processes found."
    }

    Write-Output "`nChecking for connected USB devices..."
    $usbDevices = Check-USBDevices
    if ($usbDevices.Count -gt 0) {
        $results += "`nConnected USB devices found:"
        foreach ($device in $usbDevices) {
            $results += $device
        }
    } else {
        $results += "`nNo connected USB devices found."
    }

    $subject = "Security Check Completed"
    $body = $results -join "`n"
    Write-Output $body
    Send-Email -subject $subject -body $body
}

# Detect the OS
$IsWindows = $false
$IsMacOS = $false
$IsLinux = $false
$OS = $PSVersionTable.OS
if ($OS -match "Windows") {
    $IsWindows = $true
} elseif ($OS -match "Darwin") {
    $IsMacOS = $true
} elseif ($OS -match "Linux") {
    $IsLinux = $true
}

# Run the main function
Main
