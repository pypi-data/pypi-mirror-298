import os
import unittest
from unittest.mock import patch
import o7util.pypi as o7pp

# coverage run -m unittest -v tests.test_pypi && coverage report && coverage html

class Pypi(unittest.TestCase):


    def test_basic(self):
        obj = o7pp.Pypi()
        version = obj.get_latest_version()
        self.assertIsInstance(version, str)

        project = obj.get_project_name()
        self.assertIsInstance(project, str)
        self.assertEqual(project, 'o7cli')

    def test_invalid(self):
        obj = o7pp.Pypi(project='o7cli-invalid-ahshr')

        with self.assertLogs(level='ERROR') as cm:
            version = obj.get_latest_version()
            self.assertIsNone(version)


        project = obj.get_project_name()
        self.assertIsInstance(project, str)
        self.assertEqual(project, 'o7cli-invalid-ahshr')




if __name__ == '__main__':
    unittest.main()
