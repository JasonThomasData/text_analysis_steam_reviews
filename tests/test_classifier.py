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
These tests make sure the classifier module works properly.
"""

class TestMnbClassifier(unittest.TestCase):
    '''
    Test this function returns a trained mnb classifier.
    We'll test this against data we've trained.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        database_manager.create_steam_reviews(db_location)
        database_manager.insert_data_steam_reviews(db_location, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
        database_manager.insert_data_steam_reviews(db_location, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'GiveMeSugar')
        database_manager.insert_data_steam_reviews(db_location, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'GiveMeSugar')

    def tearDown(self):
        db_location = 'database_test.db'
        database_manager.drop_steam_reviews(db_location)

    def test(self):
        db_location = 'database_test.db'
        reviews_to_retrieve = 16
        reviews_to_test = 4
        training_documents, testing_documents, training_classes, testing_classes = data_prep.prep_for_classifiers(db_location, reviews_to_retrieve, reviews_to_test)

        vectorizer = TfidfVectorizer()
        train_vectors = vectorizer.fit_transform(training_documents)
        negative_test_vector = vectorizer.transform(['It was bad'])
        positive_test_vector = vectorizer.transform(['It was great'])

        classifier = train_classify_data.train_mnb(train_vectors, training_classes)

        prediction_one = classifier.predict(negative_test_vector)
        prediction_two = classifier.predict(positive_test_vector)

        assert prediction_one == 'Not Recommended'
        assert prediction_two == 'Recommended'

if __name__ == '__main__':
    unittest.main()

