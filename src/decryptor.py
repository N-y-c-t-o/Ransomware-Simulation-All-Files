#!/usr/bin/env python3
"""
manual_decrypt.py - Decrypt files encrypted with AES-256-CBC
"""

import os
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

# Paste your BASE64-ENCODED key here (from the attacker server or encryption output)
# The IV is stored at the beginning of each encrypted file
BASE64_ENCODED_KEY = 'ODPQ5tDQQhyRPVncSsTW182YqkQx0e229OG2AQGQeAM='  # Replace with your actual base64 key

# Decode the key from base64 to get the actual binary key
DECRYPTION_KEY = base64.b64decode(BASE64_ENCODED_KEY)

# Define the same folders that were encrypted
TARGET_DIRS = [
    os.path.expanduser('~\\Desktop'),
    os.path.expanduser('~\\Documents'),
    os.path.expanduser('~\\Pictures'),
    os.path.expanduser('~\\Videos'),
    os.path.expanduser('~\\Downloads'),
]

# Files to delete (clean up evidence)
FILES_TO_DELETE = [
    os.path.expanduser('~\\Desktop\\READ_ME_SIMULATION.txt'),
    os.path.expanduser('~\\Desktop\\DECRYPTION_KEY.txt')
]

def decrypt_file(encrypted_path, output_path):
    """Decrypt a single file using AES-256-CBC."""
    try:
        # Read the encrypted file
        with open(encrypted_path, 'rb') as f:
            iv = f.read(16)  # First 16 bytes is the IV (stored by encryptor)
            encrypted_data = f.read()  # Rest is the encrypted data
        
        # Create AES cipher in CBC mode
        cipher = AES.new(DECRYPTION_KEY, AES.MODE_CBC, iv)
        
        # Decrypt the data
        decrypted_padded_data = cipher.decrypt(encrypted_data)
        
        # Remove padding
        decrypted_data = unpad(decrypted_padded_data, AES.block_size)
        
        # Write decrypted data to original file
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        print(f"✓ Decrypted: {os.path.basename(encrypted_path)}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to decrypt {encrypted_path}: {e}")
        return False

def find_encrypted_files(directory):
    """Recursively find all .encrypted files in a directory."""
    encrypted_files = []
    if not os.path.exists(directory):
        return encrypted_files
        
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.encrypted'):
                encrypted_files.append(os.path.join(root, file))
    return encrypted_files

def cleanup_evidence():
    """Delete ransom note and decryption key file."""
    print("\n Cleaning up evidence...")
    deleted_count = 0
    
    for file_path in FILES_TO_DELETE:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"✓ Deleted: {os.path.basename(file_path)}")
                deleted_count += 1
        except Exception as e:
            print(f"✗ Could not delete {file_path}: {e}")
    
    return deleted_count

def main():
    total_decrypted = 0
    total_failed = 0
    
    print(" Starting decryption process...")
    print(f"Using AES-256-CBC decryption")
    print(f"Key (base64): {base64.b64encode(DECRYPTION_KEY).decode()}\n")
    
    # Decrypt files in all target directories
    for target_dir in TARGET_DIRS:
        print(f" Scanning: {target_dir}")
        encrypted_files = find_encrypted_files(target_dir)
        
        if not encrypted_files:
            print("  No encrypted files found\n")
            continue
            
        print(f"  Found {len(encrypted_files)} encrypted files")
        
        for encrypted_file in encrypted_files:
            original_file = encrypted_file[:-10]  # Remove .encrypted extension
            
            if decrypt_file(encrypted_file, original_file):
                os.remove(encrypted_file)  # Delete encrypted version
                total_decrypted += 1
            else:
                total_failed += 1
        
        print()  # Empty line for readability
    
    # Clean up ransom note and key file
    deleted_files = cleanup_evidence()
    
    # Print summary
    print("\n Decryption Complete!")
    print(f"   Files successfully decrypted: {total_decrypted}")
    print(f"   Files failed to decrypt: {total_failed}")
    print(f"   Evidence files removed: {deleted_files}")
    
    if total_failed == 0:
        print("\n✅ All files have been restored successfully!")
    else:
        print(f"\n⚠️  {total_failed} files could not be decrypted. Check the errors above.")

if __name__ == "__main__":
    main()
