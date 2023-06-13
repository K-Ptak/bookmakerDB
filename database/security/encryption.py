from cryptography.fernet import Fernet


def encrypt_to_file(filename, path):
    with open(path, 'rb') as enckey:
        key = enckey.read()
    fernet = Fernet(key)

    with open(filename, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def encrypt_value(value, path):
    with open(path, 'rb') as enckey:
        key = enckey.read()
    fernet = Fernet(key)
    return fernet.encrypt(value)
