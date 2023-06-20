import mysql.connector
from security.decryption import decrypt_value


class DatabasePointer:
    credentials = []
    db = 0

    def __init__(self):
        f = open("storage/credentials.txt", "r")
        data = f.readline()
        data = decrypt_value(data, "storage/enckey.key")
        DatabasePointer.credentials = data.decode().split('\r\n')
        DatabasePointer.db = self.mysql_connect()

    @staticmethod
    def mysql_connect():
        try:
            mydb = mysql.connector.connect(
                host=DatabasePointer.credentials[0],
                user=DatabasePointer.credentials[1],
                password=DatabasePointer.credentials[2],
                database=DatabasePointer.credentials[3]
            )
        except:
            print("Cannot connect to database")
            return None
        else:
            return mydb

    @staticmethod
    def mysql_select(column="", table="", conditions=""):
        dbcursor = DatabasePointer.db.cursor()
        if column and table and conditions:
            dbcursor.execute(f"SELECT {column} FROM {table} {conditions}")
        elif column and table:
            dbcursor.execute(f"SELECT {column} FROM {table}")
        elif table:
            dbcursor.execute(f"SELECT * FROM {table}")
        else:
            return "mysql_select Error!"

        result = [item[0] for item in dbcursor.fetchall()]
        return result

    @staticmethod
    def mysql_insert(table, columns, values, params):
        if table and columns and values and params:
            dbcursor = DatabasePointer.db.cursor()
            query = f"INSERT INTO {table}({columns}) VALUES ({values})"
            dbcursor.execute(query, params)
            DatabasePointer.db.commit()
            return "Insert operation successful"
        else:
            return "mysql_insert Error!"

# k = DatabasePointer()
# print(k.mysql_select(column="id", table="user", conditions="where id=1"))
# print(k.mysql_select(column="id", table="user"))
# print(k.mysql_select(table="user"))
# print(k.mysql_select())
# print(k.mysql_insert(table="user",
#                     columns="`id`, `user_password`, `user_login`, `user_firstname`, `user_surname`, `user_email`, `user_phone_number`, `user_balance`, `user_admin`",
#                     values="'3', '1', '1', '1', '1', '1', '1', '1', '1'"))
