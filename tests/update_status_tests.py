import unittest
from slack.updater import StatusUpdater


class TestStatusUpdater(unittest.TestCase):

    def setUp(self):
        self.updater = StatusUpdater(token='example-token',
                                     email='email@example.com')

    def test_find_user(self):
        self.assertEqual(self.updater.find_user_by_email(), 'ABC123', "User ID doesn't match")

    def test_set_status(self):
        self.updater.update_status(status='Test status')
        self.assertEqual(self.updater.display_status(), 'Test status',
                         'status was not set correctly')


if __name__ == '__main__':
    unittest.main()