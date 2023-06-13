import mysql.connector


class DatabasePointer:
    def __init__(self):
        f = open("storage/credentials.txt", "r")
        credentials = []
        for x in f:
            credentials.append(x)

    @staticmethod
    def mysql_connect(credentials):
        mydb = mysql.connector.connect(
            host=credentials[0],
            user=credentials[1],
            password=credentials[2],
            database=credentials[3]
        )
        return mydb
