import unittest
from server import *


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server(socket.gethostbyname(socket.gethostname()), 31415)
        self.client = Client(server)
        self.connection = self.client.connnection
        self.user = User("Andrzej", "Stopka", True, ["raz", "dwa", "trzy"])

    def test_clear_inbox(self):
        user_inbox = ["dasfad", "dsaasddas", "dsaasdasasd"]

        server.clear_inbox(self.connection, self.user)
        result = len(user_inbox)


        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()

