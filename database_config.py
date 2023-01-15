import psycopg2

class UserDatabase():
    connection = psycopg2.connect(user="postgres", password="superuser", host="127.0.0.1", port="5432", dbname="users")
    cursor = connection.cursor()

    def create_user_table(self):
        create_table_query = """CREATE TABLE users
        (NAME TEXT PRIMARY KEY NOT NULL,
        PASSWORD TEXT NOT NULL,
        ADMIN BOOL NOT NULL,
        INBOX text[][]);"""

        self.cursor.execute(create_table_query)
        self.connection.commit()
        print("Table was created")

    def add_user(self, username, password, admin, mail_box):
        add_user_query = f"""INSERT INTO users 
        (NAME, PASSWORD, ADMIN, INBOX) 
        VALUES(%s,%s,%s,%s);"""
        record_to_insert = (username, password, admin, mail_box)
        self.cursor.execute(add_user_query, record_to_insert)
        self.connection.commit()
        print("User was added")


user_database = UserDatabase()

# user_database.create_user_table()
# user_database.add_user("Andrzej", "Stopka", False, [])
user_database.add_user("Ania", "Stopka", True, ["hej co tam", "admin"])


TRZEBA ZROBIĆ jako dictionary mail_box

