from cryptography.fernet import Fernet


def decrypt_to_file(filename):
    with open('database/storage/enckey.key', 'rb') as enckey:
        key = enckey.read()
    fernet = Fernet(key)

    with open(filename, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(filename, 'wb') as dec_file:
        dec_file.write(decrypted)


def decrypt_value(value):
    with open('database/storage/enckey.key', 'rb') as enckey:
        key = enckey.read()
    fernet = Fernet(key)
    return fernet.decrypt(value)
