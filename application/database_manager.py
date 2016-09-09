#! usr/bin/env python3

import sqlite3

def create_steam_reviews(db):
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS steam_reviews (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, app_num INTEGER, date_scraped TEXT, classified INTEGER, user_recommendation TEXT, user_review_text TEXT, user_name TEXT);')

def drop_steam_reviews(db):
    cur = db.cursor()
    cur.execute('DROP TABLE steam_reviews;')

def insert_data_steam_reviews(db, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name):
    cur = db.cursor()
    query = "INSERT INTO steam_reviews (url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name) VALUES (?,?,?,?,?,?,?);"
    data = (url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)
    cur.execute(query, data)
    db.commit()

def remove_duplicates_steam_reviews(db):
    '''
    In theory, we should never need to do this, because the scraper would filter out any duplicates as it goes.
    This can be done to make sure there are no duplicates if concerned the scraper hasn't worked.
    This may be useful to test that scraper functionality has worked.
    '''

    cur = db.cursor()
    query = "DELETE FROM steam_reviews WHERE id NOT IN (SELECT MAX(id) FROM steam_reviews GROUP BY user_name, user_recommendation, user_review_text);"
    cur.execute(query)
    db.commit()

def retrieve_one_steam_review(db, user_recommendation, classified):
    cur = db.cursor()
    query = "SELECT * FROM steam_reviews WHERE user_recommendation=? AND classified=?;"
    data = (user_recommendation, classified)
    cur.execute(query, data)
    return cur.fetchone()

def retrieve_last_steam_reviews(db):
    cur = db.cursor()
    query = "SELECT * FROM steam_reviews ORDER BY id DESC LIMIT 1;"
    cur.execute(query)
    return cur.fetchone()
