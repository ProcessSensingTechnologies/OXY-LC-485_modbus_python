from oxy_lc.utilities.conversions import twos_compliment
import unittest

class TestTwosCompliment(unittest.TestCase):
    def test_twenty(self):
        self.assertEqual(twos_compliment(20, 16), 20)

    def test_minus_forty(self):
        self.assertEqual(twos_compliment(65496, 16), -40)


if __name__ == "__main__":
    unittest.main()
