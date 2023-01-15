import psycopg2
from psycopg2.extras import Json


class Database():
    connection = psycopg2.connect(user="postgres", password="superuser", host="127.0.0.1", port="5432", dbname="users")
    cursor = connection.cursor()

    def create_user_table(self):
        create_table_query = """CREATE TABLE users
        (NAME TEXT PRIMARY KEY NOT NULL,
        PASSWORD TEXT NOT NULL,
        ADMIN BOOL NOT NULL,
        INBOX json);"""

        self.cursor.execute(create_table_query)
        self.connection.commit()

    def load_data(self):
        load_data_query = """SELECT * FROM users"""
        self.cursor.execute(load_data_query)
        return self.cursor.fetchall()

    def add_user(self, username, password, admin, mail_box):
        add_user_query = f"""INSERT INTO users 
        (NAME, PASSWORD, ADMIN, INBOX) 
        VALUES(%s,%s,%s,%s);"""
        record_to_insert = (username, password, admin, Json(mail_box))
        self.cursor.execute(add_user_query, record_to_insert)
        self.connection.commit()

    def reset_password(self, user):
        reset_password_query = """UPDATE users
        SET password = %s, 
        inbox = inbox || %s
        WHERE name = %s"""
        
        self.cursor.execute(reset_password_query, ("newpassword", Json({"type your new password": "Admin"}), user))
        self.connection.commit()

        Ogarnąć reset password do bazy

    def set_password(self, user, password):
        set_password_query = """UPDATE users
        SET password = %s
        WHERE name = %s"""
        self.cursor.execute(set_password_query, (password, user))
        self.connection.commit()



database = Database()

# database.create_user_table()
# database.add_user("Andrzej", "Stopka", False, {"hej": "admin", "co tam": "andrzej"})
# database.add_user("Ania", "Stopka", True, {"hej co tam": "admin", "eluwa": "andrzej"})
# database.add_user("Tymon", "Stopka", True, dict())

# database.reset_password()








