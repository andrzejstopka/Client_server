import unittest
from server import *


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = server
        self.andrzej = User("Andrzej", "Stopka", True, [("hej", "Ania"), ("cześć", "Ania")])
        self.ania = User("Ania", "Stopka", False, [])
        self.tymon = User("Tymon", "Stopka", False, [("type your new password", "Admin")])
        server.all_users = [self.andrzej, self.ania]

    def test_create_account(self):
        account_data_1 = {"Andrzej": "Stopka"}
        account_data_2 = {"Tymon": "Stopka"}

        result_1 = self.server.create_account(account_data_1)
        result_2 = self.server.create_account(account_data_2)

        self.assertFalse(result_1)
        self.assertTrue(result_2)
    
    def test_login(self):
        login_data_1 = {"Andrzej": "Stopka"}
        login_data_2 = {"Andrzej": "Andrzej"}
        login_data_3 = {"Andrzej": "reset"}

        result_1 = self.server.login(login_data_1)
        result_2 = self.server.login(login_data_2)
        result_3 = self.server.login(login_data_3)

        self.assertIsInstance(result_1, User)
        self.assertFalse(result_2)
        self.assertIsNone(result_3)

    def test_send_message(self):
        recipient_1 = {"Ania": "hej"}
        recipient_2 = {"Tymon": "hej"}

        result_1 = self.server.send_message(self.andrzej, recipient_1)
        result_2 = self.server.send_message(self.andrzej, recipient_2)
        result_3 = self.server.send_message(self.andrzej, {"Andrzej": "hej"})

        self.assertEqual(result_1, "Your message has been sent!".encode("utf-8"))
        self.assertEqual(result_2, "There is no such user".encode("utf8"))
        self.assertEqual(result_3, "You can't send a message to yourself".encode("utf8"))

    def test_read_message(self):

        result_1 = self.server.read_message(self.andrzej)
        result_2 = self.server.read_message(self.ania)
        result_3 = self.server.read_message(self.tymon)
        
        self.assertIsInstance(result_1, dict)
        self.assertEqual(result_2, {"[INFO]": "You don't have any messages"})
        self.assertEqual(result_3, {})

if __name__ == "__main__":
    unittest.main()

