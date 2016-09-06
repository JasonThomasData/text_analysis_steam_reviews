#! usr/bin/env python3

import sqlite3

def create_reviews_table(db):
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS steam_reviews (id serial PRIMARY KEY, url text, date_scraped text, user_recommendation text, user_review_text text, user_review_date text);')

def drop_reviews_table(db):
    cur = db.cursor()
    cur.execute('DROP TABLE steam_reviews;')

def insert_data_reviews_table(db, url, date_scraped, user_recommendation, user_review_text, user_review_date):
    cur = db.cursor()
    query = "INSERT INTO steam_reviews (url, date_scraped, user_recommendation, user_review_text, user_review_date) VALUES (?,?,?,?,?);"
    data = (url, date_scraped, user_recommendation, user_review_text, user_review_date)
    cur.execute(query, data)
