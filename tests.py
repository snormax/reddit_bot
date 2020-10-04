import unittest
import main


class Test(unittest.TestCase):

    # Testing rps()
    def test_rps_rvp(self):
        return_value = main.rps('username_a', 'rock', 'username_b', 'paper')
        self.assertEqual(return_value, 'username_b')

    def test_rps_pvr(self):
        return_value = main.rps('username_a', 'paper', 'username_b', 'rock')
        self.assertEqual(return_value, 'username_a')

    def test_rps_svp(self):
        return_value = main.rps('username_a', 'scissors', 'username_b', 'paper')
        self.assertEqual(return_value, 'username_a')

    def test_rps_pvs(self):
        return_value = main.rps('username_a', 'paper', 'username_b', 'scissors')
        self.assertEqual(return_value, 'username_b')

    # Testing parse_body()
    def test_body_parse_valid(self):
        return_value = main.parse_body('u/rps_duel_bot afufi apgharg fjaeogj u/test')
        self.assertEqual(return_value, 'test')

    def test_body_parse_invalid(self):
        return_value = main.parse_body('u/rps_duel_bot afufi apgharg fjaeogj')
        self.assertEqual(return_value, '-1')

    def test_body_parse_no_username(self):
        return_value = main.parse_body('afufi apgharg fjaeogj')
        self.assertEqual(return_value, '-1')

    def test_body_parse_none(self):
        return_value = main.parse_body(None)
        self.assertEqual(return_value, '-1')


if __name__ == '__main__':
    unittest.main()
