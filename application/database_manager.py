#! usr/bin/env python3

import sqlite3

def create_reviews_table(db):
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS steam_reviews (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, date_scraped TEXT, classified INTEGER, user_recommendation TEXT, user_review_text TEXT, user_name TEXT);')

def drop_reviews_table(db):
    cur = db.cursor()
    cur.execute('DROP TABLE steam_reviews;')

def insert_data_reviews_table(db, url, date_scraped, classified, user_recommendation, user_review_text, user_name):
    cur = db.cursor()
    query = "INSERT INTO steam_reviews (url, date_scraped, classified, user_recommendation, user_review_text, user_name) VALUES (?,?,?,?,?,?);"
    data = (url, date_scraped, classified, user_recommendation, user_review_text, user_name)
    cur.execute(query, data)
