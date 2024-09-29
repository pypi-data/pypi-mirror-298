import os
import unittest
from unittest.mock import patch
import o7util.run as o7r

# coverage run -m unittest -v tests.test_run && coverage report && coverage html

class Run(unittest.TestCase):


    def test_No_Timeout(self):
        test = o7r.run('sleep 0.5', shell = True)
        self.assertEqual(test[0], 0)

    def test_Timeout_NotExpired(self):
        test = o7r.run('sleep 0.5', shell = True, timeout = 2)
        self.assertEqual(test[0], 0)

    def test_Timeout_Expired(self):
        test = o7r.run('sleep 1', shell = True, timeout = 1)
        self.assertEqual(test[0], -9)

    def test_NotExistingFile(self):
        test = o7r.run('./cdkhceiukhui.shs', shell = False, timeout = 1)
        self.assertNotEqual(test[0], 0)

    # def test_timeout_expired_on_nt(self):
    #     os.name = 'nt'
    #     with patch('subprocess.run') as mock:
    #         mock.return_value = None
    #         test = o7r.run('sleep 2', shell = True, timeout = 1)
    #     self.assertEqual(test[0], -9)

class GetProcessChilc(unittest.TestCase):

    def test_basic(self):
        test = o7r.get_process_children(os.getpid())
        self.assertIsInstance(test, list)

if __name__ == '__main__':
    unittest.main()
