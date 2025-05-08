# **USB Auto-Execution Payload - Beginner's Guide**  
**For Authorized Penetration Testing Labs Only**  

---

## **📌 Table of Contents**  
1. [What This Does](#-what-this-does)  
2. [Requirements](#-requirements)  
3. [Step-by-Step Setup](#-step-by-step-setup)  
4. [How to Use](#-how-to-use)  
5. [Safety Notes](#⚠️-safety-notes)  

---

## **🔍 What This Does**  
This tool creates a **hidden program** that:  
✅ Automatically runs when a USB is plugged in (no clicks needed)  
✅ Connects to your computer secretly (for authorized testing)  
✅ Can run commands you send it  
✅ Hides itself completely (no windows or popups)  

**Legal Use Only**: Designed for Hack The Box, CTF challenges, or cybersecurity labs with permission.  

---

## **📋 Requirements**  
### **🛠️ Tools Needed**  
1. **Windows 10/11 PC** (for testing)  
2. **USB Flash Drive** (formatted as FAT32)  
3. **Python 3.8+** ([Download here](https://www.python.org/downloads/))  
4. **Git** (optional, [Download here](https://git-scm.com/))  

### **📦 Python Libraries**  
Install these first:  
```bash
pip install pyinstaller pycryptodomex pywin32
```

---

## **🔧 Step-by-Step Setup**  

### **1️⃣ Generate RSA Keys**  
*(Skip if you already have a key pair)*  

#### **Method A: Using Python**  
Run this in a Python shell:  
```python
from Cryptodome.PublicKey import RSA
key = RSA.generate(2048)
print("Public Key:\n", key.publickey().export_key().decode())
```  
➡️ **Copy the printed public key** (save it for Step 2).  

#### **Method B: Using OpenSSL (Advanced)**  
```bash
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
```  
➡️ Open `public.pem` and copy its contents.  

---

### **2️⃣ Update `lab.py`**  
1. Open `lab.py` in a text editor (like Notepad++ or VS Code).  
2. Find this section:  
   ```python
   RSA_PUB_KEY = """-----BEGIN PUBLIC KEY-----
   PASTE_YOUR_2048_BIT_PUBLIC_KEY_HERE
   -----END PUBLIC KEY-----"""
   ```  
3. **Paste your public key** between the `"""` quotes.  
   - ✅ **Must include** `BEGIN/END PUBLIC KEY` lines.  
   - ❌ **No extra spaces** before/after the key.  

---

### **3️⃣ Compile to EXE**  
1. Open **Command Prompt** in the folder where `lab.py` is saved.  
2. Run:  
   ```bash
   pyinstaller --onefile --noconsole --clean lab.py -n payload
   ```  
   This creates `payload.exe` in the `dist` folder.  

---

### **4️⃣ Prepare the USB**  
1. **Format USB as FAT32** (Right-click → Format → FAT32).  
2. Copy `payload.exe` to the **root of the USB** (not inside any folder).  
3. **First Run Setup**:  
   - Plug USB into your test machine.  
   - Manually run `payload.exe` **once**. It will:  
     - Create hidden `autorun.inf` and `launch.bat` files.  
     - Set up auto-run for future USB insertions.  

---

## **🚀 How to Use**  
### **🔌 Auto-Run on USB Insertion**  
After the first setup:  
1. Plug the USB into any **test machine**.  
2. The payload runs **automatically** (no clicks needed).  
3. Check your C2 server for connections.  

### **🖥️ Manual Testing**  
1. Run `payload.exe` directly on the test machine.  
2. It will:  
   - Hide itself (no windows).  
   - Connect to your C2 server.  

### **📡 C2 Server Commands**  
Send these from your server:  
- `exec [command]`: Run system commands (e.g., `exec whoami`).  
- `cleanup`: Remove traces and exit.  

---

## **⚠️ Safety Notes**  
1. **Only use in authorized environments** (labs, HTB, CTFs).  
2. **Disable autorun on personal PCs**:  
   ```powershell
   Set-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer -Name NoDriveTypeAutoRun -Value 0x95
   ```  
3. **Clean up after testing**:  
   - The payload auto-removes traces when done.  
   - Format the USB afterward.  

---

## **❓ Troubleshooting**  
| Error | Fix |  
|-------|-----|  
| `No module 'Cryptodome'` | Run `pip install pycryptodomex` |  
| `Incorrect padding` | Regenerate RSA keys and paste correctly |  
| USB doesn’t auto-run | Enable autorun in VM:  
  ```powershell
  Set-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer -Name NoDriveTypeAutoRun -Value 0
  ```  

---

## **📜 Final Notes**  
- Test in a **virtual machine** first (e.g., VirtualBox).  
- Document all activity for your lab reports.  
- **Never use this on systems without permission.**  

🔐 **Happy ethical hacking!**  

--- 

**✉️ Need help?**  
Ask your instructor or lab supervisor for guidance.
