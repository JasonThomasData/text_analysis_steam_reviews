#! usr/bin/env python3

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
    
    db_location = 'database_steam_reviews.db'
    with sqlite3.connect(db_location, timeout=20) as db:
        recommended_reviews = database_manager.retrieve_steam_reviews(db, 'Recommended', 0, review_quantity)
        not_recommended_reviews = database_manager.retrieve_steam_reviews(db, 'Not Recommended', 0, review_quantity)

    return recommended_reviews, not_recommended_reviews
