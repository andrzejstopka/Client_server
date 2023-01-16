import psycopg2
from psycopg2.extras import Json



class Database():
    connection = psycopg2.connect(user="postgres", password="superuser", host="127.0.0.1", port="5432", dbname="clientserver")
    cursor = connection.cursor()

    def create_user_table(self):
        create_table_query = """CREATE TABLE users
        (NAME TEXT PRIMARY KEY NOT NULL,
        PASSWORD TEXT NOT NULL,
        ADMIN BOOL NOT NULL,
        INBOX jsonb);"""

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
        inbox = inbox::jsonb || '{"type your new password":"Admin"}'
        WHERE name = %s"""

        record_to_execute = ("newpassword", user)
        self.cursor.execute(reset_password_query, record_to_execute)
        self.connection.commit()
    
    def set_password(self, user, password):
        set_password_query = """UPDATE users
        SET password = %s
        WHERE name = %s"""
        self.cursor.execute(set_password_query, (password, user))
        self.connection.commit()

    def become_admin(self, user):
        become_admin_query = """UPDATE users
        SET admin = %s
        WHERE name = %s"""

        self.cursor.execute(become_admin_query, (True, user))
        self.connection.commit()

    def send_message(self, message_data, recipient):
        send_message_query = """UPDATE users
        SET inbox = inbox::jsonb || %s
        where name = %s"""
        record_to_execute = (Json(message_data), recipient)
        self.cursor.execute(send_message_query, record_to_execute)
        self.connection.commit()
    
    def send_to_all(self, message):
        send_to_all_query = """UPDATE users
        SET inbox = inbox::jsonb || %s
        where admin = %s"""
        record_to_execute = (Json({message: "admin"}), False)
        self.cursor.execute(send_to_all_query, record_to_execute)
        self.connection.commit()
    
    def delete_user(self, user):
        delete_user_query = "DELETE FROM users WHERE name = %s"

        self.cursor.execute(delete_user_query, (user,))
        self.connection.commit()
    
    def clear_inbox(self, user):
        clear_inbox_query = "UPDATE users SET inbox = %s WHERE name = %s"
        self.cursor.execute(clear_inbox_query, (Json({}), user))
        self.connection.commit()

database = Database()

database.clear_inbox("ania")









