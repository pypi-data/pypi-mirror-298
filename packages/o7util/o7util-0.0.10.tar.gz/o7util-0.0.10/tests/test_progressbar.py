import unittest
from unittest.mock import patch

import mock
import pytest

import o7util.progressbar

# coverage run -m unittest -v tests.test_progressbar && coverage report && coverage html

class Test_Progressbar(unittest.TestCase):

    @patch('sys.stdout.write')
    @patch('sys.stdout.flush')
    def test_basic(self, *args):
        bar = o7util.progressbar.ProgressBar()
        bar.kick()
        bar.kick(inc=0)


    def test_main(self):

        with mock.patch.object(o7util.progressbar, "__name__", "__main__"):
            # Test the main function
            o7util.progressbar.main()


if __name__ == '__main__':
    unittest.main()
