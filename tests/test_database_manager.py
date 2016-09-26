#! usr/bin/env python3

import os
import sys
import unittest
import sqlite3
import atexit

# Here we're moving the context into the parent folder
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from application import database_manager
from application import scraper

from archive import data_prep
from archive import train_classify_data

from sklearn.feature_extraction.text import TfidfVectorizer

@atexit.register
def goodbye():
    try:
        os.remove('database_test.db')
    except FileNotFoundError:
        pass

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
        database_manager.create_steam_reviews(db_location)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            cur = db.cursor()
            response = cur.execute("SELECT 1 FROM steam_reviews LIMIT 1;")
            response_no_data = response.fetchone()
            assert response_no_data is None

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)


class TestInsertOneData(unittest.TestCase):
    '''
    Tests we can insert one piece of data into this db.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        database_manager.create_steam_reviews(db_location)

    def test(self):
        db_location = 'database_test.db'

        url = 'url'
        app_num = 300000
        date_scraped = 'today'
        user_recommendation = 'great'
        user_review_text = 'great'
        user_name = 'Bob'
        classified = 0
        database_manager.insert_data_steam_reviews(db_location, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)

        with sqlite3.connect(db_location, timeout=20) as db:
            cur = db.cursor()
            response = cur.execute("SELECT * FROM steam_reviews;")
            response_one_data = response.fetchone()
            assert response_one_data == (1, 'url', 300000, 'today', 0, 'great', 'great', 'Bob')

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)

class TestInsertTwoData(unittest.TestCase):
    '''
    Tests we can insert two pieces of data into this db.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        database_manager.create_steam_reviews(db_location)

    def test(self):
        db_location = 'database_test.db'

        url = 'url'
        app_num = 300000
        date_scraped = 'today'
        user_recommendation = 'great'
        user_review_text = 'great'
        user_name = 'Bob'
        classified = 0
        database_manager.insert_data_steam_reviews(db_location, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)
        database_manager.insert_data_steam_reviews(db_location, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)

        with sqlite3.connect(db_location, timeout=20) as db:
            cur = db.cursor()
            response = cur.execute("SELECT * FROM steam_reviews;")
            response_all_data = response.fetchall()
            assert response_all_data[0] == (1, 'url', 300000, 'today', 0, 'great', 'great', 'Bob')
            assert response_all_data[1] == (2, 'url', 300000, 'today', 0, 'great', 'great', 'Bob')

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)


class TestRetrieveDataOne(unittest.TestCase):
    '''
    Tests we can retrieve data from db.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        database_manager.create_steam_reviews(db_location)

    def test(self):
        db_location = 'database_test.db'

        url = 'url'
        app_num = 300000
        date_scraped = 'today'
        user_recommendation = 'Recommended'
        user_review_text = 'great'
        user_name = 'Bob'
        classified = 0
        database_manager.insert_data_steam_reviews(db_location, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)

        response = database_manager.retrieve_steam_reviews(db_location, 'Recommended', 0, 1)
        assert response[0] == (1, 'url', 300000, 'today', 0, 'Recommended', 'great', 'Bob')

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)

class TestRetrieveDataOneFail1(unittest.TestCase):
    '''
    The previous test works, but this returns len(response) == 0 because the WHERE condition in the function is false, 
    because of recommendation.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        database_manager.create_steam_reviews(db_location)

    def test(self):
        db_location = 'database_test.db'

        url = 'url'
        app_num = 300000
        date_scraped = 'today'
        user_recommendation = 'Not Recommended'
        user_review_text = 'great'
        user_name = 'Bob'
        classified = 0
        database_manager.insert_data_steam_reviews(db_location, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)

        response = database_manager.retrieve_steam_reviews(db_location, 'Recommended', 0, 1)
        assert len(response) == 0

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)


class TestRetrieveDataOneFail2(unittest.TestCase):
    '''
    The first of these tests works, but this returns len(response) == 0 because the WHERE condition in the function is false, 
    because of categorised.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        database_manager.create_steam_reviews(db_location)

    def test(self):
        db_location = 'database_test.db'

        url = 'url'
        app_num = 300000
        date_scraped = 'today'
        user_recommendation = 'Recommended'
        user_review_text = 'great'
        user_name = 'Bob'
        classified = 1
        database_manager.insert_data_steam_reviews(db_location, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)

        response = database_manager.retrieve_steam_reviews(db_location, 'Recommended', 0, 1)
        assert len(response) == 0

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)


class TestRetrieveDataBatch1(unittest.TestCase):
    '''
    Test batch retrieval of data from db.    
    '''

    def setUp(self):
        db_location = 'database_test.db'
        database_manager.create_steam_reviews(db_location)
        database_manager.insert_data_steam_reviews(db_location, 'url_1', 300000, '2011-01-01', 0, 'Not Recommended', 'It was great', 'Destroyer')
        database_manager.insert_data_steam_reviews(db_location, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_3', 300025, '2011-01-01', 0, 'Not Recommended', 'OMG', 'Makiavelli')
        database_manager.insert_data_steam_reviews(db_location, 'url_4', 300040, '2011-01-01', 0, 'Not Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_5', 300040, '2011-01-01', 0, 'Not Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')
        database_manager.insert_data_steam_reviews(db_location, 'url_6', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
        database_manager.insert_data_steam_reviews(db_location, 'url_7', 300020, '2011-01-01', 0, 'Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_8', 300025, '2011-01-01', 0, 'Recommended', 'OMG', 'Makiavelli')
        database_manager.insert_data_steam_reviews(db_location, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')

    def test(self):
        db_location = 'database_test.db'
        response = database_manager.retrieve_steam_reviews(db_location, 'Not Recommended', 0, 3)
        assert len(response) == 3

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)


class TestRetrieveDataBatch2(unittest.TestCase):
    '''
    Test batch retrieval of data from db.    
    '''

    def setUp(self):
        db_location = 'database_test.db'
        database_manager.create_steam_reviews(db_location)
        database_manager.insert_data_steam_reviews(db_location, 'url_1', 300000, '2011-01-01', 0, 'Not Recommended', 'It was great', 'Destroyer')
        database_manager.insert_data_steam_reviews(db_location, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_3', 300025, '2011-01-01', 0, 'Not Recommended', 'OMG', 'Makiavelli')
        database_manager.insert_data_steam_reviews(db_location, 'url_4', 300040, '2011-01-01', 0, 'Not Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_5', 300040, '2011-01-01', 0, 'Not Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')
        database_manager.insert_data_steam_reviews(db_location, 'url_6', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
        database_manager.insert_data_steam_reviews(db_location, 'url_7', 300020, '2011-01-01', 0, 'Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_8', 300025, '2011-01-01', 0, 'Recommended', 'OMG', 'Makiavelli')
        database_manager.insert_data_steam_reviews(db_location, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')

    def test(self):
        db_location = 'database_test.db'
        response = database_manager.retrieve_steam_reviews(db_location, 'Recommended', 0, 7)
        assert len(response) == 5

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)


class TestRetrieveDataBatch3(unittest.TestCase):
    '''
    Test batch retrieval of data from db.    
    '''

    def setUp(self):
        db_location = 'database_test.db'
        database_manager.create_steam_reviews(db_location)
        database_manager.insert_data_steam_reviews(db_location, 'url_1', 300000, '2011-01-01', 0, 'Not Recommended', 'It was great', 'Destroyer')
        database_manager.insert_data_steam_reviews(db_location, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_3', 300025, '2011-01-01', 0, 'Not Recommended', 'OMG', 'Makiavelli')
        database_manager.insert_data_steam_reviews(db_location, 'url_4', 300040, '2011-01-01', 0, 'Not Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_5', 300040, '2011-01-01', 0, 'Not Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')
        database_manager.insert_data_steam_reviews(db_location, 'url_6', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
        database_manager.insert_data_steam_reviews(db_location, 'url_7', 300020, '2011-01-01', 0, 'Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_8', 300025, '2011-01-01', 0, 'Recommended', 'OMG', 'Makiavelli')
        database_manager.insert_data_steam_reviews(db_location, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')

    def test(self):
        db_location = 'database_test.db'
        response = database_manager.retrieve_steam_reviews(db_location, 'Recommended', 0, 2)
        assert len(response) == 2

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)


class TestRetrieveDataOnePosOneNeg(unittest.TestCase):
    '''
    Test retrieval of one positive and one negative review from db.
    The function returns a list of length one, since the fetchall function is used.
    So, results[0] will give you the result.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        database_manager.create_steam_reviews(db_location)
        database_manager.insert_data_steam_reviews(db_location, 'url_1', 300000, '2011-01-01', 0, 'Not Recommended', 'It was Awful', 'Destroyer')
        database_manager.insert_data_steam_reviews(db_location, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_4', 300040, '2011-01-01', 0, 'Not Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_5', 300040, '2011-01-01', 0, 'Not Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')
        database_manager.insert_data_steam_reviews(db_location, 'url_6', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Creater')
        database_manager.insert_data_steam_reviews(db_location, 'url_8', 300025, '2011-01-01', 0, 'Recommended', 'OMG', 'Makiavelli')
        database_manager.insert_data_steam_reviews(db_location, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'More, More, More', 'GiveMeSalt')
        database_manager.insert_data_steam_reviews(db_location, 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'Loved it. Would play again', 'Speedy99')

    def test(self):
        db_location = 'database_test.db'
        pos_review = database_manager.retrieve_steam_reviews(db_location, 'Recommended', 0, 1)
        neg_review = database_manager.retrieve_steam_reviews(db_location, 'Not Recommended', 0, 1)
        assert pos_review[0][6] == 'Loved it. Would play again'
        assert neg_review[0][6] == 'When I get out of this padded cell I will bake a cake'

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)


class TestRetrieveLastRow(unittest.TestCase):
    '''
    Tests we can retrieve the last row in the table. We need this as a record of what has been scraped.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        database_manager.create_steam_reviews(db_location)
        database_manager.insert_data_steam_reviews(db_location, 'url_1', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
        database_manager.insert_data_steam_reviews(db_location, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_3', 300025, '2011-01-01', 0, 'Recommended', 'OMG', 'Makiavelli')

    def test(self):
        db_location = 'database_test.db'
        response = database_manager.retrieve_last_steam_review(db_location)
        assert response == (3, 'url_3', 300025, '2011-01-01', 0, 'Recommended', 'OMG', 'Makiavelli')

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)


class TestDeleteDuplicatesInDB(unittest.TestCase):
    '''
    Tests duplicate rows in the DB will be deleted.
    Some pages will have double-ups of the same review, we need to delete those.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        database_manager.create_steam_reviews(db_location)
        database_manager.insert_data_steam_reviews(db_location, 'url_1', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
        database_manager.insert_data_steam_reviews(db_location, 'url_1', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
        database_manager.insert_data_steam_reviews(db_location, 'url_1', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')

    def test(self):
        db_location = 'database_test.db'
        database_manager.remove_duplicates_steam_reviews(db_location)
        with sqlite3.connect(db_location, timeout=20) as db:
            cur = db.cursor()
            response = cur.execute("SELECT * FROM steam_reviews WHERE app_num = 300000;")

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)


class TestScraperDeleteDuplicateReviews(unittest.TestCase):
    '''
    Tests duplicate reviews in the DB will be deleted.
    Some pages will have double-ups of the same review, we need to delete those.
    This test has two duplicates.
    '''

    def test(self):
        list_of_reviews = [
            {
                'user_recommendation': 'Recommended',
                'user_review_text': 'It is great',
                'user_name': 'bahumbug'
            },
            {
                'user_recommendation': 'Recommended',
                'user_review_text': 'It is great',
                'user_name': 'bahumbug'
            },
            {
                'user_recommendation': 'Not Recommended',
                'user_review_text': 'This is the worst thing that has ever happened.',
                'user_name': 'WhatYouWantSonny'
            },
            {
                'user_recommendation': 'Recommended',
                'user_review_text': 'DAMN BUY THIS GAME',
                'user_name': 'pimplePopper61'
            },
            {
                'user_recommendation': 'Not Recommended',
                'user_review_text': 'This is the worst thing that has ever happened.',
                'user_name': 'WhatYouWantSonny'
            }
        ]

        reviews_no_duplicates = scraper.remove_duplicates(list_of_reviews)
        assert len(reviews_no_duplicates) == 3

        try:
            assert reviews_no_duplicates[0]['user_recommendation'] == 'Recommended'
            assert reviews_no_duplicates[1]['user_recommendation'] == 'Not Recommended'
        except TypeError:
            assert False #this means the responses are not dicts, which means this fails


if __name__ == '__main__':
    unittest.main()
