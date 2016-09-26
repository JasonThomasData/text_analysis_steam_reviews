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
These tests are for the data_prep module.
"""

class TestDataPrepRetrieveEqual(unittest.TestCase):
    '''
    Tests the function that retrieves an equal number of 'Recommended' and 'Not Recommended' reviews.
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

        recommended_reviews, not_recommended_reviews = data_prep.retrieve_reviews_balanced(db_location, 4)
        assert len(recommended_reviews) == 2
        assert len(not_recommended_reviews) == 2
        assert not_recommended_reviews[0][5] == 'Not Recommended'
        assert not_recommended_reviews[1][5] == 'Not Recommended'
        assert recommended_reviews[0][5] == 'Recommended'
        assert recommended_reviews[1][5] == 'Recommended'

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)


class TestDataPrepFormListsForTraining(unittest.TestCase):
    '''
    Tests the function that splits the lists of Recommended and Not Recommended reviews and combines
    them into a list of training_data (large) and test_data (size equal to interval).
    Both are equally formed of 'Recommended' and 'Not Recommended'
    '''

    def test(self):
        recommended_reviews = ['Recommeded review'] * 300
        not_recommended_reviews = ['Not recommeded review'] * 300
        interval = 100

        training_data, test_data = data_prep.form_training_test_lists(recommended_reviews, not_recommended_reviews, interval)

        assert len(training_data) == 500
        assert len(test_data) == 100


class TestDataPrepTransposeLists(unittest.TestCase):
    '''
    Tests our data is transposed as expected.
    '''

    def test(self):
        training_data = [('row id', 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'Sluggish666')] * 100
        testing_data = [('row id', 'url', 300000, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Destroyer')] * 100

        training_data_transposed, testing_data_transposed = data_prep.transpose_data(training_data, testing_data)

        assert training_data_transposed[5][20] == 'Recommended'
        assert training_data_transposed[6][40] == 'It was great'
        assert training_data_transposed[5][50] == 'Recommended'
        assert testing_data_transposed[5][60] == 'Not Recommended'
        assert testing_data_transposed[6][70] == 'It was bad'
        assert testing_data_transposed[5][80] == 'Not Recommended'

class TestDataPrepExtractClasses(unittest.TestCase):
    '''
    Tests our training_data_classes and testing_data_classes are returned as expected.
    '''

    def test(self):
        training_data = [('row id', 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'Sluggish666')] * 100
        testing_data = [('row id', 'url', 300000, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Destroyer')] * 100

        training_data_transposed, testing_data_transposed = data_prep.transpose_data(training_data, testing_data)

        training_data_classes, testing_data_classes = data_prep.extract_classes(training_data_transposed, testing_data_transposed)

        assert len(training_data_classes) == 100
        assert len(testing_data_classes) == 100


class TestDataPrepExtractClasses(unittest.TestCase):
    '''
    Tests our training_data_documents and testing_data_documents are returned as expected.
    '''

    def test(self):
        training_data = [('row id', 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'Sluggish666')] * 100
        testing_data = [('row id', 'url', 300000, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Destroyer')] * 100

        training_data_transposed, testing_data_transposed = data_prep.transpose_data(training_data, testing_data)

        training_data_documents, testing_data_documents = data_prep.extract_reviews(training_data_transposed, testing_data_transposed)

        assert len(training_data_documents) == 100
        assert len(testing_data_documents) == 100


class TestDataPrepControllerFunction1(unittest.TestCase):
    '''
    Tests the main controller function processes and returns data. Classifier module will use this.
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

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)

    def test(self):
        db_location = 'database_test.db'
        reviews_to_retrieve = 8
        reviews_to_test = 4
        training_data_documents, testing_data_documents, training_data_classes, testing_data_classes = data_prep.prep_for_classifiers(db_location, reviews_to_retrieve, reviews_to_test)
        assert len(training_data_documents) == 4
        assert len(testing_data_documents) == 4
        assert len(training_data_classes) == 4
        assert len(testing_data_classes) == 4


class TestDataPrepControllerFunction2(unittest.TestCase):
    '''
    Tests the main controller function processes and returns data. Classifier module will use this.
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
        database_manager.insert_data_steam_reviews(db_location, 'url_11', 300040, '2011-01-01', 0, 'Not Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_12', 300040, '2011-01-01', 0, 'Not Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')
        database_manager.insert_data_steam_reviews(db_location, 'url_13', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
        database_manager.insert_data_steam_reviews(db_location, 'url_14', 300020, '2011-01-01', 0, 'Recommended', 'It was bad', 'Dismantler')


    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)

    def test(self):
        db_location = 'database_test.db'
        reviews_to_retrieve = 12
        reviews_to_test = 4
        training_data_documents, testing_data_documents, training_data_classes, testing_data_classes = data_prep.prep_for_classifiers(db_location, reviews_to_retrieve, reviews_to_test)
        assert len(training_data_documents) == 8
        assert len(testing_data_documents) == 4
        assert len(training_data_classes) == 8
        assert len(testing_data_classes) == 4


if __name__ == '__main__':
    unittest.main()
