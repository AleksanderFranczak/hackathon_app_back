from flask_sqlalchemy import SQLAlchemy
import sqlite3

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    db.create_all()

db_cn = sqlite3.connect("test.db")
db_cr = db_cn.cursor()

DB_SETUP = False

#! If base DB_SETUP = False -> execute create tables
def init_databse():
    pass


def add_user_to_db(email, password):
    pass


def user_in_db(email, password):
    pass