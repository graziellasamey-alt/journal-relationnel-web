from models.db import get_db


def create_resources_table():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            description TEXT NOT NULL,
            file_path TEXT NOT NULL,
            target_year TEXT NOT NULL,
            target_scope TEXT NOT NULL CHECK(target_scope IN ('field', 'all')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


def create_resource(user_id, title, subject, resource_type, description, file_path, target_year, target_scope):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resources (
            user_id, title, subject, resource_type, description, file_path, target_year, target_scope
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, title, subject, resource_type, description, file_path, target_year, target_scope))

    conn.commit()
    resource_id = cursor.lastrowid
    conn.close()
    return resource_id


def get_resource_by_id(resource_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.*, u.nom, u.prenom, u.field_of_study, u.study_year
        FROM resources r
        JOIN users u ON r.user_id = u.id
        WHERE r.id = ?
    """, (resource_id,))

    resource = cursor.fetchone()
    conn.close()
    return resource


def get_recent_resources(user_field_of_study=None, search=None, resource_type=None, target_year=None):
    conn = get_db()
    cursor = conn.cursor()

    query = """
        SELECT r.*, u.nom, u.prenom, u.field_of_study, u.study_year
        FROM resources r
        JOIN users u ON r.user_id = u.id
        WHERE 1=1
    """
    params = []

    if user_field_of_study:
        query += """
            AND (
                r.target_scope = 'all'
                OR (r.target_scope = 'field' AND u.field_of_study = ?)
            )
        """
        params.append(user_field_of_study)

    if resource_type:
        query += " AND r.resource_type = ?"
        params.append(resource_type)

    if search:
        query += " AND (r.title LIKE ? OR r.subject LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term])

    if target_year:
        query += " AND r.target_year = ?"
        params.append(target_year)

    query += " ORDER BY r.created_at DESC"

    cursor.execute(query, tuple(params))
    resources = cursor.fetchall()
    conn.close()
    return resources


def get_user_resources(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM resources
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))

    resources = cursor.fetchall()
    conn.close()
    return resources


def delete_resource(resource_id, user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM resources
        WHERE id = ? AND user_id = ?
    """, (resource_id, user_id))

    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted > 0

