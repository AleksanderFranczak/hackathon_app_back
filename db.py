import sqlite3

db = sqlite3.connect("test.db")
db_cr = db.cursor()

DB_SETUP = False

#! If base DB_SETUP = False -> execute create tables
def init_databse():
    pass


def add_user_to_db(email, password):
    pass


def user_in_db(email, password):
    pass