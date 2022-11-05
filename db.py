# import sqlite3

# db_cn = sqlite3.connect("./instance/project.db")
# db_cr = db_cn.cursor()
from app import db
from app import Users

def add_user_to_db(**kwargs):
    try:
        user = Users(**kwargs)
        db.session.add(user)
        db.session.commit()
    except Exception as err:
        raise err
    return 0


def user_in_db(name, email, password, nr_phone, description, address_id):
    pass