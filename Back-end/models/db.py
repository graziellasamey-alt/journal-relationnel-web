import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(INSTANCE_DIR, "database.db")


def get_db():
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    from models.user_model import create_users_table
    from models.question_model import create_questions_table
    from models.resource_model import create_resources_table
    from models.favorite_model import (
        create_favorite_questions_table,
        create_favorite_resources_table
    )

    create_users_table()
    create_questions_table()
    create_resources_table()
    create_favorite_questions_table()
    create_favorite_resources_table()