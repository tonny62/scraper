import unittest
from src.sql import *
from src.taskcreator import *

class Taskcreator_Test(unittest.TestCase):
    '''Do tests on module src/taskcreator.'''

    def test_get_tasks_test(self):
        tasks = read_testdata()
        self.assertEqual(len(tasks), 60810)



class SQL_Test(unittest.TestCase):
    '''Do tests on module src/sql.'''

    def setUp(self):
        self.cnx = get_connection()

    def test_connection(self):
        with self.assertRaises(Exception):
            try:
                cursor = self.cnx.cursor()
            except:
                # if caught exception will not raise and make this test fail
                pass
            else:
                # else raise to make this test success
                raise


if(__name__ == '__main__'):
    unittest.main()

