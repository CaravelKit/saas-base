import os
import unittest
import tempfile

# This is non-working code, reserved for the future use
from usersite import common

class ScaffoldTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_accountyaml(self):
        res = True
        try:
            common.read_account_settings()
        except Exception as e:
            print(e)
            res = False
        assert res == True

if __name__ == '__main__':
    unittest.main()