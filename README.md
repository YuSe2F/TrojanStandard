# **USB Auto-Execution Payload - HTB/CTS Lab**

## **Overview**
This is a professional penetration testing payload designed for **authorized cybersecurity training environments** like Hack The Box (HTB) and Certified Threat Specialist (CTS) labs. The payload provides silent USB auto-execution capabilities with encrypted command and control (C2) communication.

**Authorized Use Only:** This tool is strictly for educational purposes in controlled lab environments with explicit permission.

## **Features**
- **Silent USB Auto-Execution** - Runs automatically when USB is inserted
- **Multi-Layer Persistence** - Registry keys + Scheduled Tasks
- **Secure C2 Communication** - RSA-2048 + AES-256 encryption
- **Advanced Stealth** - No windows, hidden process, spoofed name
- **Self-Cleaning** - Automatic removal of artifacts

## **Prerequisites**
- Python 3.8+
- Windows 10/11 lab environment
- Administrator access (for persistence installation)
- PyInstaller (`pip install pyinstaller`)

## **Installation**
1. Clone/download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## **Configuration**
Edit these values in `lab.py`:
```python
C2_SERVER = "YOUR_C2_IP"  # Your control server IP
C2_PORT = 443             # Communication port
USB_ID = "HTB_CTS_LAB_001" # Unique identifier for your assignment
```

## **Compilation**
```bash
pyinstaller --onefile --noconsole --clean lab.py -n payload
```

## **Deployment**
1. Format USB drive as FAT32
2. Copy these files to USB root:
   - `dist/payload.exe`
3. Insert USB into target machine and run once manually to setup autorun

## **Expected Behavior**
1. On first run:
   - Creates hidden `autorun.inf` and `launch.bat`
   - Installs persistence mechanisms
   - Connects to C2 server

2. Subsequent USB insertions:
   - Payload runs automatically
   - Establishes secure C2 channel
   - No visible indication of execution

## **Command and Control**
The payload supports these C2 commands:
- `exec [command]` - Execute system command
- `cleanup` - Remove persistence and exit
- `upload [path]` - Upload file to target
- `download [path]` - Download file from target

## **Cleanup**
The payload automatically:
1. Removes registry persistence
2. Deletes scheduled tasks
3. Self-destructs when compiled version completes

## **Detection Prevention**
- Process name spoofing (appears as `svchost.exe`)
- Random network jitter (avoids pattern detection)
- Encrypted communications (RSA+AES hybrid)
- Hidden file attributes

## **Lab Testing Notes**
1. Enable autorun in test VMs:
   ```powershell
   Set-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer -Name NoDriveTypeAutoRun -Value 0
   ```
2. Monitor with:
   ```powershell
   Get-ScheduledTask -TaskName "WindowsDefenderUpdate"
   Get-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Run
   ```

## **Disclaimer**
This tool is provided solely for:
- Authorized penetration testing training
- Cybersecurity education
- Controlled lab environments

Unauthorized use is strictly prohibited. Always obtain proper permissions before testing.

## **License**
This project is licensed under the **YuSe2F Lab Agreement** - for educational use only.
