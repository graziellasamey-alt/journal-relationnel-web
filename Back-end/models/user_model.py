from models.db import get_db


def create_users_table():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            field_of_study TEXT NOT NULL,
            study_year TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def create_user(nom, prenom, email, password_hash, field_of_study, study_year):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (nom, prenom, email, password_hash, field_of_study, study_year)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nom, prenom, email, password_hash, field_of_study, study_year))

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def get_user_by_email(email):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()
    conn.close()
    return user


def update_user_profile(user_id, prenom, nom, email, study_year, field_of_study):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET prenom = ?, nom = ?, email = ?, study_year = ?, field_of_study = ?
        WHERE id = ?
    """, (prenom, nom, email, study_year, field_of_study, user_id))

    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()

    return updated


def get_all_users():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        ORDER BY created_at DESC
    """)

    users = cursor.fetchall()
    conn.close()
    return users