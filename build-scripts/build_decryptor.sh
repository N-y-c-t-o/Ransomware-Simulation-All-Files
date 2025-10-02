For Decryption
wine pyinstaller --onefile --windowed --name=FileRecoveryTool \
    --hidden-import=Cryptodome \
    --hidden-import=Cryptodome.Cipher \
    --hidden-import=Cryptodome.Cipher.AES \
    --hidden-import=Cryptodome.Util.Padding \
    --hidden-import=base64 \
    decryptor.py