#! usr/bin/env python3

'''
This module contains more functions that I would usually have, because I wanted to
make sure the process of preparing the data for classification was explained as
well as possible. Having more functions also allows to have more specific tests.
'''

from application import database_manager
import sqlite3
import numpy as np

start_interval = 200
end_interval = 5100
interval = 100

def retrieve_reviews_balanced(db, reviews_to_train):
    '''
    Retrieves an equal number of 'Recommended' and 'Not Recommended' reviews rows. 
    These are the entire rows from the db.
    You should take care to make sure there are enough available.
    If 'Not Recommended' has fewer in the db than 'Recommended', 
    then the total number of reviews to process should be no larger than double that.
    '''

    review_quantity = int(reviews_to_train / 2)
    
    recommended_reviews = database_manager.retrieve_steam_reviews(db, 'Recommended', 0, review_quantity)
    not_recommended_reviews = database_manager.retrieve_steam_reviews(db, 'Not Recommended', 0, review_quantity)

    return recommended_reviews, not_recommended_reviews


def form_training_test_lists(recommended_reviews, not_recommended_reviews, interval):
    '''
    We need traing and test lists. The training_data must be half made of 'Recommeded'
    and 'Not Recommended' reviews. So too must the test_data.
    The test data must be the size of the interval.
    '''

    interval_split = int(interval / 2)

    training_data = recommended_reviews[interval_split:] + not_recommended_reviews[interval_split:]
    testing_data = recommended_reviews[:interval_split] + not_recommended_reviews[:interval_split]

    return training_data, testing_data


def transpose_data(training_data, testing_data):
    '''
    This will turn each list from a list of n-size tuples, to an n-size list of lists.
    '''
    
    training_data_transposed = np.transpose(training_data)
    testing_data_transposed = np.transpose(testing_data)

    return training_data_transposed, testing_data_transposed
