from models.db import get_db


def create_questions_table():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            target_year TEXT NOT NULL,
            target_scope TEXT NOT NULL CHECK(target_scope IN ('field', 'all')),
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def create_question(user_id, title, subject, target_year, target_scope, description):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO questions (user_id, title, subject, target_year, target_scope, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, title, subject, target_year, target_scope, description))

    conn.commit()
    question_id = cursor.lastrowid
    conn.close()
    return question_id


def get_question_by_id(question_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT q.*, u.nom, u.prenom, u.field_of_study, u.study_year
        FROM questions q
        JOIN users u ON q.user_id = u.id
        WHERE q.id = ?
    """, (question_id,))

    question = cursor.fetchone()
    conn.close()
    return question


def get_recent_questions(user_field_of_study=None, search=None):
    conn = get_db()
    cursor = conn.cursor()

    query = """
        SELECT 
            q.*, 
            u.nom, 
            u.prenom, 
            u.field_of_study, 
            u.study_year,
            COUNT(a.id) AS answers_count
        FROM questions q
        JOIN users u ON q.user_id = u.id
        LEFT JOIN answers a ON q.id = a.question_id
        WHERE 1=1
    """
    params = []

    if user_field_of_study:
        query += """
            AND (
                q.target_scope = 'all'
                OR (q.target_scope = 'field' AND u.field_of_study = ?)
            )
        """
        params.append(user_field_of_study)

    if search:
        query += " AND (q.title LIKE ? OR q.subject LIKE ? OR q.description LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term])

    query += """
        GROUP BY q.id
        ORDER BY q.created_at DESC
    """
    print("QUERY =", query)
    print("PARAMS =", params)

    cursor.execute(query, tuple(params))
    questions = cursor.fetchall()
    conn.close()
    return questions

def get_user_questions(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM questions
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))

    questions = cursor.fetchall()
    conn.close()
    return questions


def delete_question(question_id, user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM questions
        WHERE id = ? AND user_id = ?
    """, (question_id, user_id))

    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted > 0