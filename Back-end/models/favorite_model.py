from models.db import get_db


def create_favorite_questions_table():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, question_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def create_favorite_resources_table():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resource_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, resource_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (resource_id) REFERENCES resources(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def is_favorite_question(user_id, question_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM favorite_questions
        WHERE user_id = ? AND question_id = ?
    """, (user_id, question_id))

    favorite = cursor.fetchone()
    conn.close()
    return favorite is not None


def is_favorite_resource(user_id, resource_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM favorite_resources
        WHERE user_id = ? AND resource_id = ?
    """, (user_id, resource_id))

    favorite = cursor.fetchone()
    conn.close()
    return favorite is not None


def toggle_favorite_question(user_id, question_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM favorite_questions
        WHERE user_id = ? AND question_id = ?
    """, (user_id, question_id))

    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            DELETE FROM favorite_questions
            WHERE user_id = ? AND question_id = ?
        """, (user_id, question_id))
        conn.commit()
        conn.close()
        return False
    else:
        cursor.execute("""
            INSERT INTO favorite_questions (user_id, question_id)
            VALUES (?, ?)
        """, (user_id, question_id))
        conn.commit()
        conn.close()
        return True


def toggle_favorite_resource(user_id, resource_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM favorite_resources
        WHERE user_id = ? AND resource_id = ?
    """, (user_id, resource_id))

    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            DELETE FROM favorite_resources
            WHERE user_id = ? AND resource_id = ?
        """, (user_id, resource_id))
        conn.commit()
        conn.close()
        return False
    else:
        cursor.execute("""
            INSERT INTO favorite_resources (user_id, resource_id)
            VALUES (?, ?)
        """, (user_id, resource_id))
        conn.commit()
        conn.close()
        return True


def get_user_favorite_questions(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            q.*,
            fq.created_at AS favorited_at,
            COUNT(a.id) AS answers_count
        FROM favorite_questions fq
        JOIN questions q ON fq.question_id = q.id
        LEFT JOIN answers a ON q.id = a.question_id
        WHERE fq.user_id = ?
        GROUP BY q.id
        ORDER BY fq.created_at DESC
    """, (user_id,))

    questions = cursor.fetchall()
    conn.close()
    return questions


def get_user_favorite_resources(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.*, fr.created_at AS favorited_at
        FROM favorite_resources fr
        JOIN resources r ON fr.resource_id = r.id
        WHERE fr.user_id = ?
        ORDER BY fr.created_at DESC
    """, (user_id,))

    resources = cursor.fetchall()
    conn.close()
    return resources

def get_user_favorite_resource_ids(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT resource_id
        FROM favorite_resources
        WHERE user_id = ?
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [row["resource_id"] for row in rows]