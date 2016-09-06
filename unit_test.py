#! usr/bin/env python3

import unittest
import sqlite3
from application import database_manager

class TestCreateDB(unittest.TestCase):
    '''
    Tests the function to create a DB in sqlite3 is working.
    '''

    def test(self):
        db_location = 'database_test.db'
        db = sqlite3.connect(db_location, timeout=20)
        rv = database_manager.create_reviews_table(db)
        assert 'record created' in rv

if __name__ == '__main__':
    unittest.main()
