from models.db import get_db


def create_answers_table():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def create_answer(question_id, user_id, content):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO answers (question_id, user_id, content)
        VALUES (?, ?, ?)
    """, (question_id, user_id, content))

    conn.commit()
    answer_id = cursor.lastrowid
    conn.close()
    return answer_id


def get_answers_by_question(question_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.*, u.nom, u.prenom
        FROM answers a
        JOIN users u ON a.user_id = u.id
        WHERE a.question_id = ?
        ORDER BY a.created_at ASC
    """, (question_id,))

    answers = cursor.fetchall()
    conn.close()
    return answers


def delete_answer(answer_id, user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM answers
        WHERE id = ? AND user_id = ?
    """, (answer_id, user_id))

    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted > 0