from cryptography.fernet import Fernet


def decrypt_to_file(filename, path):
    with open(path, 'rb') as enckey:
        key = enckey.read()
    fernet = Fernet(key)

    with open(filename, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(filename, 'wb') as dec_file:
        dec_file.write(decrypted)


def decrypt_value(value, path):
    with open(path, 'rb') as enckey:
        key = enckey.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(value)

    return decrypted
