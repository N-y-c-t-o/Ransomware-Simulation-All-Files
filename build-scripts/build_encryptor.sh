For Encryption
wine pyinstaller --onefile --windowed --name=SausageMan \
    --hidden-import=Cryptodome \
    --hidden-import=Cryptodome.Cipher \
    --hidden-import=Cryptodome.Cipher.AES \
    --hidden-import=Cryptodome.Util \
    --hidden-import=Cryptodome.Util.Padding \
    --hidden-import=Cryptodome.Random \
    --hidden-import=PIL \
    --hidden-import=PIL.Image \
    --hidden-import=PIL.ImageDraw \
    --hidden-import=PIL.ImageFont \
    invoice_checker.py --icon=logo.jpeg