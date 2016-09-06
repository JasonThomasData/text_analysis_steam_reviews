#! usr/bin/env python3

import unittest
import sqlite3
from application import database_manager

"""
These first tests are for the database_manager module. We need the DB before scraping any data.
"""

class TestCreateDB(unittest.TestCase):
    '''
    Tests the function to create a DB in sqlite3 is working.
    We now have a database with nothing in it.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_reviews_table(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            cur = db.cursor()
            response = cur.execute("SELECT 1 FROM steam_reviews LIMIT 1;")
            response_no_data = response.fetchone()
            assert response_no_data is None

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_reviews_table(db)


class TestInsertOneData(unittest.TestCase):
    '''
    Tests we can insert one piece of data into this db.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_reviews_table(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:

            url = 'url'
            date_scraped = 'today'
            user_recommendation = 'great'
            user_review_text = 'great'
            user_review_date = 'yesterday'
            classified = 0
            database_manager.insert_data_reviews_table(db, url, date_scraped, classified, user_recommendation, user_review_text, user_review_date)

            cur = db.cursor()
            response = cur.execute("SELECT * FROM steam_reviews;")
            response_one_data = response.fetchone()
            assert response_one_data == (1, 'url', 'today', 0, 'great', 'great', 'yesterday')

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_reviews_table(db)


class TestInsertTwoData(unittest.TestCase):
    '''
    Tests we can insert two pieces of data into this db.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_reviews_table(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:

            url = 'url'
            date_scraped = 'today'
            user_recommendation = 'great'
            user_review_text = 'great'
            user_review_date = 'yesterday'
            classified = False
            database_manager.insert_data_reviews_table(db, url, date_scraped, classified, user_recommendation, user_review_text, user_review_date)
            database_manager.insert_data_reviews_table(db, url, date_scraped, classified, user_recommendation, user_review_text, user_review_date)

            cur = db.cursor()
            response = cur.execute("SELECT * FROM steam_reviews;")
            response_all_data = response.fetchall()
            assert response_all_data[0] == (1, 'url', 'today', 0, 'great', 'great', 'yesterday')
            assert response_all_data[1] == (2, 'url', 'today', 0, 'great', 'great', 'yesterday')

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_reviews_table(db)



if __name__ == '__main__':
    unittest.main()
