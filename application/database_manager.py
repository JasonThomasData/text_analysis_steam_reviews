#! usr/bin/env python3

import sqlite3

#db_location = 'database_test.db'
#db = sqlite3.connect(db_location, timeout=20)
#cur = db.cursor()

def create_reviews_table(db):
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS steam_reviews (id serial PRIMARY KEY, url text, date_scraped text, user_recommendation text, user_review_text text, user_name text, user_review_date text);')