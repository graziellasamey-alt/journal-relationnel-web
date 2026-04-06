from werkzeug.security import generate_password_hash
from models.db import get_db

def seed():
    conn = get_db()
    cursor = conn.cursor()

    # USERS
    users = [
        ("SAMEY", "Graziella", "graziella.samey@etu.univ-amu.fr", generate_password_hash("password123"), "Informatique", "L2"),
        ("Dupont", "Jean", "jean.dupont@etu.univ-amu.fr", generate_password_hash("password123"), "Informatique", "L1"),
        ("Martin", "Claire", "claire.martin@etu.univ-amu.fr", generate_password_hash("password123"), "Mathématiques", "L3"),
        ("Bernard", "Lucas", "lucas.bernard@etu.univ-amu.fr", generate_password_hash("password123"), "Informatique", "M1"),
        ("Moreau", "Sarah", "sarah.moreau@etu.univ-amu.fr", generate_password_hash("password123"), "Physique", "L2"),
    ]

    for nom, prenom, email, password, field_of_study, study_year in users:
        cursor.execute("""
            INSERT OR IGNORE INTO users (nom, prenom, email, password_hash, field_of_study, study_year)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom, prenom, email, password, field_of_study, study_year))

    # récupérer ids users
    cursor.execute("SELECT id, email FROM users")
    user_map = {row["email"]: row["id"] for row in cursor.fetchall()}

    # QUESTIONS
    questions = [
        (user_map["graziella.samey@etu.univ-amu.fr"], "Comment utiliser Flask Blueprints ?", "Développement web", "L2", "field", "Je ne comprends pas bien comment séparer les routes avec les blueprints."),
        (user_map["jean.dupont@etu.univ-amu.fr"], "Différence entre list et tuple en Python ?", "Python", "L1", "field", "Je veux comprendre dans quels cas utiliser une liste ou un tuple."),
        (user_map["lucas.bernard@etu.univ-amu.fr"], "C'est quoi une clé étrangère en base de données ?", "Base de données", "L1", "field", "Pouvez-vous expliquer simplement la notion de clé étrangère ?"),
        (user_map["graziella.samey@etu.univ-amu.fr"], "Comment faire un CRUD en Flask ?", "Développement web", "L2", "field", "Je veux afficher, ajouter, modifier et supprimer des données avec Flask."),
        (user_map["jean.dupont@etu.univ-amu.fr"], "Quelle est la différence entre GET et POST ?", "Développement web", "L1", "field", "Je vois souvent ces deux méthodes en HTML et Flask."),
    ]

    for user_id, title, subject, target_year, target_scope, description in questions:
        cursor.execute("""
            INSERT INTO questions (user_id, title, subject, target_year, target_scope, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, title, subject, target_year, target_scope, description))

    # ANSWERS
    cursor.execute("SELECT id, title FROM questions")
    question_map = {row["title"]: row["id"] for row in cursor.fetchall()}

    answers = [
        (user_map["jean.dupont@etu.univ-amu.fr"], question_map["Comment utiliser Flask Blueprints ?"], "Les blueprints permettent d'organiser les routes par module."),
        (user_map["lucas.bernard@etu.univ-amu.fr"], question_map["Différence entre list et tuple en Python ?"], "Une list est modifiable, un tuple non."),
        (user_map["graziella.samey@etu.univ-amu.fr"], question_map["C'est quoi une clé étrangère en base de données ?"], "C'est une colonne qui référence la clé primaire d'une autre table."),
    ]

    for user_id, question_id, content in answers:
        cursor.execute("""
            INSERT INTO answers (user_id, question_id, content)
            VALUES (?, ?, ?)
        """, (user_id, question_id, content))

    # RESSOURCES
    resources = [
        (user_map["graziella.samey@etu.univ-amu.fr"], "TD Python bases", "Python", "TD", "Fichier d'exercices pour s'entraîner sur les bases de Python.", "td_python.pdf", "L1", "field"),
        (user_map["jean.dupont@etu.univ-amu.fr"], "Résumé Flask", "Développement web", "Fiche", "Résumé de cours sur Flask et les routes.", "resume_flask.pdf", "L2", "field"),
        (user_map["lucas.bernard@etu.univ-amu.fr"], "Sujet examen SQL", "Base de données", "Examen", "Ancien sujet d'examen SQL pour révision.", "sql_exam.pdf", "L2", "field"),
        (user_map["graziella.samey@etu.univ-amu.fr"], "TP HTML CSS", "Développement web", "TP", "TP simple pour pratiquer HTML et CSS.", "tp_html_css.pdf", "L1", "field"),
    ]

    for user_id, title, subject, resource_type, description, file_path, target_year, target_scope in resources:
        cursor.execute("""
            INSERT INTO resources (user_id, title, subject, resource_type, description, file_path, target_year, target_scope)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, title, subject, resource_type, description, file_path, target_year, target_scope))

    # FAVORIS QUESTIONS
    favorite_questions = [
        (user_map["graziella.samey@etu.univ-amu.fr"], question_map["Différence entre list et tuple en Python ?"]),
        (user_map["graziella.samey@etu.univ-amu.fr"], question_map["Quelle est la différence entre GET et POST ?"]),
    ]

    for user_id, question_id in favorite_questions:
        cursor.execute("""
            INSERT OR IGNORE INTO favorite_questions (user_id, question_id)
            VALUES (?, ?)
        """, (user_id, question_id))

    # FAVORIS RESSOURCES
    cursor.execute("SELECT id, title FROM resources")
    resource_map = {row["title"]: row["id"] for row in cursor.fetchall()}

    favorite_resources = [
        (user_map["graziella.samey@etu.univ-amu.fr"], resource_map["Résumé Flask"]),
        (user_map["graziella.samey@etu.univ-amu.fr"], resource_map["Sujet examen SQL"]),
    ]

    for user_id, resource_id in favorite_resources:
        cursor.execute("""
            INSERT OR IGNORE INTO favorite_resources (user_id, resource_id)
            VALUES (?, ?)
        """, (user_id, resource_id))

    conn.commit()
    conn.close()
    print("Fake data ajoutées avec succès.")

if __name__ == "__main__":
    seed()