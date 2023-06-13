import mysql.connector
from security.decryption import decrypt_value


class DatabasePointer:
    def __init__(self):
        f = open("storage/credentials.txt", "r")
        data = f.readline()
        data = decrypt_value(data, "storage/enckey.key")
        credentials = data.decode().split('\r\n')

    @staticmethod
    def mysql_connect(credentials):
        mydb = mysql.connector.connect(
            host=credentials[0],
            user=credentials[1],
            password=credentials[2],
            database=credentials[3]
        )
        return mydb


k = DatabasePointer()
