from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open('../storage/enckey.key', 'wb') as enckey:
    enckey.write(key)
