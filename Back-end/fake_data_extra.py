from werkzeug.security import generate_password_hash
from models.db import get_db


def safe_get_question_id(cursor, title):
    cursor.execute("SELECT id FROM questions WHERE title = ?", (title,))
    row = cursor.fetchone()
    return row["id"] if row else None


def safe_get_resource_id(cursor, title):
    cursor.execute("SELECT id FROM resources WHERE title = ?", (title,))
    row = cursor.fetchone()
    return row["id"] if row else None


def seed_extra():
    conn = get_db()
    cursor = conn.cursor()

    # =========================
    # 1) USERS - nouveaux uniquement
    # =========================
    users = [
        # INFORMATIQUE (gros volume)
        ("Lambert", "Nora", "nora.lambert@etu.univ-amu.fr", "Informatique", "L1"),
        ("Meyer", "Yanis", "yanis.meyer@etu.univ-amu.fr", "Informatique", "L1"),
        ("Roux", "Lina", "lina.roux@etu.univ-amu.fr", "Informatique", "L1"),
        ("Fontaine", "Noah", "noah.fontaine@etu.univ-amu.fr", "Informatique", "L1"),
        ("Andre", "Mael", "mael.andre@etu.univ-amu.fr", "Informatique", "L1"),
        ("Garnier", "Sofia", "sofia.garnier@etu.univ-amu.fr", "Informatique", "L2"),
        ("Chevalier", "Ilyes", "ilyes.chevalier@etu.univ-amu.fr", "Informatique", "L2"),
        ("Francois", "Lea", "lea.francois@etu.univ-amu.fr", "Informatique", "L2"),
        ("Leclerc", "Adam", "adam.leclerc@etu.univ-amu.fr", "Informatique", "L2"),
        ("Mercier", "Aya", "aya.mercier@etu.univ-amu.fr", "Informatique", "L2"),
        ("Blanc", "Rayan", "rayan.blanc@etu.univ-amu.fr", "Informatique", "L2"),
        ("Henry", "Mila", "mila.henry@etu.univ-amu.fr", "Informatique", "L2"),
        ("Renaud", "Amine", "amine.renaud@etu.univ-amu.fr", "Informatique", "L3"),
        ("Giraud", "Salome", "salome.giraud@etu.univ-amu.fr", "Informatique", "L3"),
        ("Perrin", "Bilal", "bilal.perrin@etu.univ-amu.fr", "Informatique", "L3"),
        ("Masson", "Jade", "jade.masson@etu.univ-amu.fr", "Informatique", "L3"),
        ("Marchand", "Iris", "iris.marchand@etu.univ-amu.fr", "Informatique", "L3"),
        ("Barbier", "Sami", "sami.barbier@etu.univ-amu.fr", "Informatique", "M1"),
        ("Colin", "Eva", "eva.colin@etu.univ-amu.fr", "Informatique", "M1"),
        ("Brun", "Nassim", "nassim.brun@etu.univ-amu.fr", "Informatique", "M1"),
        ("Paris", "Manon", "manon.paris@etu.univ-amu.fr", "Informatique", "M1"),
        ("Picard", "Walid", "walid.picard@etu.univ-amu.fr", "Informatique", "M2"),
        ("Fabre", "Louna", "louna.fabre@etu.univ-amu.fr", "Informatique", "M2"),
        ("Aubry", "Kylian", "kylian.aubry@etu.univ-amu.fr", "Informatique", "M2"),
        ("Noel", "Sarah", "sarah.noel@etu.univ-amu.fr", "Informatique", "M2"),

        # AUTRES FILIÈRES
        ("Schmitt", "Camille", "camille.schmitt@etu.univ-amu.fr", "Mathématiques", "L1"),
        ("Boyer", "Thibault", "thibault.boyer@etu.univ-amu.fr", "Mathématiques", "L2"),
        ("Arnaud", "Meryem", "meryem.arnaud@etu.univ-amu.fr", "Mathématiques", "L3"),
        ("Lemoine", "Kenza", "kenza.lemoine@etu.univ-amu.fr", "Physique", "L1"),
        ("Menard", "Thomas", "thomas.menard@etu.univ-amu.fr", "Physique", "L2"),
        ("Dupuis", "Nina", "nina.dupuis@etu.univ-amu.fr", "Physique", "L3"),
        ("Legrand", "Yacine", "yacine.legrand@etu.univ-amu.fr", "Chimie", "L1"),
        ("Navarro", "Alicia", "alicia.navarro@etu.univ-amu.fr", "Chimie", "L2"),
        ("Bourgeois", "Mehdi", "mehdi.bourgeois@etu.univ-amu.fr", "Médecine", "L2"),
        ("Gauthier", "Imane", "imane.gauthier@etu.univ-amu.fr", "Médecine", "M1"),
    ]

    default_password_hash = generate_password_hash("password123")

    for nom, prenom, email, field_of_study, study_year in users:
        cursor.execute("""
            INSERT OR IGNORE INTO users (nom, prenom, email, password_hash, field_of_study, study_year)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom, prenom, email, default_password_hash, field_of_study, study_year))

    cursor.execute("SELECT id, email FROM users")
    user_map = {row["email"]: row["id"] for row in cursor.fetchall()}

    # =========================
    # 2) QUESTIONS - toutes nouvelles
    # =========================
    questions = [
        # Informatique L1/L2/L3/M1/M2
        ("nora.lambert@etu.univ-amu.fr", "Comment installer Flask dans un environnement virtuel ?", "Python", "L1", "field", "Je débute et je veux comprendre les étapes avec venv."),
        ("yanis.meyer@etu.univ-amu.fr", "À quoi sert un fichier requirements.txt ?", "Python", "L1", "field", "Je vois souvent ce fichier dans les projets Python mais je ne comprends pas son utilité."),
        ("lina.roux@etu.univ-amu.fr", "Comment utiliser render_template avec Flask ?", "Développement web", "L1", "field", "Je voudrais afficher une page HTML correctement."),
        ("noah.fontaine@etu.univ-amu.fr", "Pourquoi utiliser url_for en Flask ?", "Développement web", "L1", "field", "Je vois url_for dans les templates et les routes mais je ne comprends pas vraiment."),
        ("mael.andre@etu.univ-amu.fr", "Quelle différence entre == et is en Python ?", "Python", "L1", "field", "J’ai du mal à voir quand utiliser l’un ou l’autre."),

        ("sofia.garnier@etu.univ-amu.fr", "Comment organiser les dossiers static et templates dans Flask ?", "Développement web", "L2", "field", "Je veux une structure propre pour mon projet."),
        ("ilyes.chevalier@etu.univ-amu.fr", "Comment faire une relation entre users et questions en SQLite ?", "Base de données", "L2", "field", "Je veux lier un utilisateur à plusieurs questions dans ma base."),
        ("lea.francois@etu.univ-amu.fr", "Comment récupérer un paramètre dans request.form ?", "Flask", "L2", "field", "Je voudrais comprendre comment traiter un formulaire HTML."),
        ("adam.leclerc@etu.univ-amu.fr", "Comment créer une session utilisateur après connexion ?", "Authentification", "L2", "field", "Je veux garder l’utilisateur connecté après login."),
        ("aya.mercier@etu.univ-amu.fr", "Pourquoi mes fichiers CSS ne se chargent pas avec Flask ?", "Développement web", "L2", "field", "Mon HTML s’affiche mais pas le style."),
        ("rayan.blanc@etu.univ-amu.fr", "Comment ajouter un système de favoris pour des questions ?", "Développement web", "L2", "field", "Je veux permettre aux utilisateurs d’ajouter des questions en favoris."),
        ("mila.henry@etu.univ-amu.fr", "Comment vérifier qu’un email AMU est valide à l’inscription ?", "Authentification", "L2", "field", "Je veux limiter l’inscription aux mails universitaires."),

        ("amine.renaud@etu.univ-amu.fr", "Comment faire une pagination sur une liste de questions Flask ?", "Développement web", "L3", "field", "Je veux afficher 10 questions par page."),
        ("salome.giraud@etu.univ-amu.fr", "Comment sécuriser les mots de passe avec Werkzeug ?", "Sécurité", "L3", "field", "Je veux savoir pourquoi on utilise generate_password_hash."),
        ("bilal.perrin@etu.univ-amu.fr", "Comment envoyer un fichier uploadé dans un dossier uploads ?", "Flask", "L3", "field", "Je veux gérer l’ajout de ressources PDF."),
        ("jade.masson@etu.univ-amu.fr", "Comment faire une recherche SQL avec LIKE ?", "Base de données", "L3", "field", "Je veux rechercher des ressources par titre ou matière."),
        ("iris.marchand@etu.univ-amu.fr", "Quelle architecture choisir pour un projet Flask étudiant ?", "Génie logiciel", "L3", "all", "Je veux quelque chose de simple mais propre pour un projet d’équipe."),

        ("sami.barbier@etu.univ-amu.fr", "Comment créer une API JSON avec Flask ?", "API", "M1", "field", "Je voudrais renvoyer des données JSON au frontend."),
        ("eva.colin@etu.univ-amu.fr", "Comment protéger une route pour les utilisateurs connectés uniquement ?", "Authentification", "M1", "field", "Je veux empêcher l’accès aux visiteurs non connectés."),
        ("nassim.brun@etu.univ-amu.fr", "Comment mettre en place une recherche multicritère ?", "Développement web", "M1", "field", "Je veux filtrer questions et ressources par année et matière."),
        ("manon.paris@etu.univ-amu.fr", "Comment gérer les erreurs 404 et 500 dans Flask ?", "Flask", "M1", "field", "Je veux des pages d’erreur personnalisées."),

        ("walid.picard@etu.univ-amu.fr", "Comment préparer un projet Flask pour le déploiement ?", "DevOps", "M2", "all", "Je voudrais savoir quoi nettoyer avant une mise en ligne."),
        ("louna.fabre@etu.univ-amu.fr", "Comment améliorer les performances d’une requête SQLite ?", "Base de données", "M2", "all", "Certaines requêtes deviennent lentes quand il y a beaucoup de données."),
        ("kylian.aubry@etu.univ-amu.fr", "Comment structurer un backend pour une plateforme étudiante ?", "Architecture logicielle", "M2", "all", "Je veux une architecture claire pour forum + ressources + profils."),
        ("sarah.noel@etu.univ-amu.fr", "Comment faire communiquer un frontend statique avec un backend Flask ?", "Développement web", "M2", "field", "Je veux intégrer mes pages HTML/CSS à mon backend."),

        # Autres filières
        ("camille.schmitt@etu.univ-amu.fr", "Comment résoudre une équation du second degré ?", "Mathématiques", "L1", "all", "J’ai besoin d’une méthode simple avec exemple."),
        ("thibault.boyer@etu.univ-amu.fr", "Comment étudier une fonction ?", "Mathématiques", "L2", "all", "Je veux une méthode claire pour dérivée, variations et limites."),
        ("meryem.arnaud@etu.univ-amu.fr", "Comment comprendre les suites numériques ?", "Mathématiques", "L3", "all", "J’ai du mal avec les suites arithmétiques et géométriques."),
        ("kenza.lemoine@etu.univ-amu.fr", "Comment appliquer les lois de Newton dans un exercice ?", "Physique", "L1", "all", "Je comprends la théorie mais pas les exercices."),
        ("thomas.menard@etu.univ-amu.fr", "Comment calculer une énergie cinétique ?", "Physique", "L2", "all", "Je veux revoir la formule avec des exemples."),
        ("nina.dupuis@etu.univ-amu.fr", "Comment réviser la mécanique pour un partiel ?", "Physique", "L3", "all", "Je cherche une bonne méthode de révision."),
        ("yacine.legrand@etu.univ-amu.fr", "Comment équilibrer une équation chimique ?", "Chimie", "L1", "all", "Je me trompe souvent dans les coefficients."),
        ("alicia.navarro@etu.univ-amu.fr", "Comment reconnaître une réaction acido-basique ?", "Chimie", "L2", "all", "Je veux des astuces simples."),
        ("mehdi.bourgeois@etu.univ-amu.fr", "Comment mémoriser l’anatomie plus efficacement ?", "Médecine", "L2", "all", "Je cherche une méthode de travail qui marche vraiment."),
        ("imane.gauthier@etu.univ-amu.fr", "Comment organiser ses fiches en médecine ?", "Médecine", "M1", "all", "Je veux une méthode propre pour réviser plusieurs modules."),
    ]

    for email, title, subject, target_year, target_scope, description in questions:
        user_id = user_map[email]
        cursor.execute("""
            INSERT INTO questions (user_id, title, subject, target_year, target_scope, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, title, subject, target_year, target_scope, description))

    cursor.execute("SELECT id, title FROM questions")
    question_map = {row["title"]: row["id"] for row in cursor.fetchall()}

    # =========================
    # 3) ANSWERS - beaucoup
    # =========================
    answers = [
        ("graziella.samey@etu.univ-amu.fr", "Comment installer Flask dans un environnement virtuel ?", "Tu peux créer un environnement avec python -m venv venv puis l’activer avant d’installer Flask avec pip."),
        ("jean.dupont@etu.univ-amu.fr", "À quoi sert un fichier requirements.txt ?", "Ce fichier sert à enregistrer les dépendances du projet pour pouvoir les réinstaller facilement."),
        ("lucas.bernard@etu.univ-amu.fr", "Comment utiliser render_template avec Flask ?", "render_template permet d’afficher un fichier HTML situé dans le dossier templates."),
        ("graziella.samey@etu.univ-amu.fr", "Pourquoi utiliser url_for en Flask ?", "url_for évite d’écrire les chemins en dur et réduit les erreurs si une route change."),
        ("emma.petit@etu.univ-amu.fr", "Quelle différence entre == et is en Python ?", "== compare les valeurs alors que is compare l’identité en mémoire."),

        ("graziella.samey@etu.univ-amu.fr", "Comment organiser les dossiers static et templates dans Flask ?", "En général on met les fichiers HTML dans templates et les CSS/JS/images dans static."),
        ("alex.durand@etu.univ-amu.fr", "Comment faire une relation entre users et questions en SQLite ?", "La table questions doit contenir une colonne user_id qui référence l’id de la table users."),
        ("graziella.samey@etu.univ-amu.fr", "Comment récupérer un paramètre dans request.form ?", "Tu peux faire request.form.get('nom_du_champ') dans ta route POST."),
        ("hugo.robert@etu.univ-amu.fr", "Comment créer une session utilisateur après connexion ?", "Après vérification du mot de passe tu stockes l’id dans session['user_id']."),
        ("graziella.samey@etu.univ-amu.fr", "Pourquoi mes fichiers CSS ne se chargent pas avec Flask ?", "Souvent le problème vient du chemin. Il faut passer par url_for('static', filename='...')."),
        ("lucas.bernard@etu.univ-amu.fr", "Comment ajouter un système de favoris pour des questions ?", "Tu peux créer une table favorite_questions avec user_id et question_id."),
        ("graziella.samey@etu.univ-amu.fr", "Comment vérifier qu’un email AMU est valide à l’inscription ?", "Tu peux vérifier que l’email se termine par @etu.univ-amu.fr ou @univ-amu.fr."),

        ("alex.durand@etu.univ-amu.fr", "Comment faire une pagination sur une liste de questions Flask ?", "Tu peux utiliser LIMIT et OFFSET côté SQL puis récupérer le numéro de page depuis request.args."),
        ("graziella.samey@etu.univ-amu.fr", "Comment sécuriser les mots de passe avec Werkzeug ?", "Il faut stocker un hash et jamais le mot de passe brut dans la base de données."),
        ("emma.petit@etu.univ-amu.fr", "Comment envoyer un fichier uploadé dans un dossier uploads ?", "Tu récupères le fichier avec request.files puis tu fais file.save(chemin)."),
        ("lucas.bernard@etu.univ-amu.fr", "Comment faire une recherche SQL avec LIKE ?", "Tu peux faire WHERE title LIKE ? avec un paramètre du style %mot%."),

        ("graziella.samey@etu.univ-amu.fr", "Comment créer une API JSON avec Flask ?", "Il suffit de retourner jsonify(donnees) dans une route."),
        ("hugo.robert@etu.univ-amu.fr", "Comment protéger une route pour les utilisateurs connectés uniquement ?", "Tu vérifies si 'user_id' est dans la session avant d’autoriser l’accès."),
        ("alex.durand@etu.univ-amu.fr", "Comment mettre en place une recherche multicritère ?", "Tu construis ta requête SQL dynamiquement en ajoutant les filtres fournis."),
        ("graziella.samey@etu.univ-amu.fr", "Comment gérer les erreurs 404 et 500 dans Flask ?", "Tu peux utiliser @app.errorhandler pour personnaliser les pages d’erreur."),
        ("lucas.bernard@etu.univ-amu.fr", "Comment faire communiquer un frontend statique avec un backend Flask ?", "Tu relies les formulaires HTML aux routes Flask et tu rends les pages avec Jinja."),

        ("claire.martin@etu.univ-amu.fr", "Comment résoudre une équation du second degré ?", "Il faut calculer le discriminant puis déterminer le nombre de solutions."),
        ("sarah.moreau@etu.univ-amu.fr", "Comment appliquer les lois de Newton dans un exercice ?", "Commence par faire le bilan des forces puis applique la deuxième loi."),
        ("nina.garcia@etu.univ-amu.fr", "Comment équilibrer une équation chimique ?", "Il faut conserver le même nombre d’atomes de chaque élément des deux côtés."),
        ("tom.fournier@etu.univ-amu.fr", "Comment mémoriser l’anatomie plus efficacement ?", "Les répétitions espacées et les schémas annotés fonctionnent très bien."),
    ]

    for email, question_title, content in answers:
        user_id = user_map.get(email)
        question_id = question_map.get(question_title)
        if user_id and question_id:
            cursor.execute("""
                INSERT INTO answers (user_id, question_id, content)
                VALUES (?, ?, ?)
            """, (user_id, question_id, content))

    # =========================
    # 4) RESSOURCES - volumineuses et différentes
    # =========================
    resources = [
        # Informatique
        ("graziella.samey@etu.univ-amu.fr", "Guide complet environnement virtuel Python", "Python", "Fiche", "Fiche claire pour créer, activer et utiliser un environnement virtuel Python.", "guide_venv_python.pdf", "L1", "field"),
        ("nora.lambert@etu.univ-amu.fr", "TD variables et conditions Python", "Python", "TD", "Exercices sur les variables, conditions et boucles en Python.", "td_variables_conditions_python.pdf", "L1", "field"),
        ("yanis.meyer@etu.univ-amu.fr", "TP fonctions Python", "Python", "TP", "Travaux pratiques sur la création et l’utilisation des fonctions.", "tp_fonctions_python.pdf", "L1", "field"),
        ("lina.roux@etu.univ-amu.fr", "Examen blanc introduction au web", "Développement web", "Examen", "Sujet d’entraînement HTML, CSS et bases du web.", "examen_blanc_intro_web.pdf", "L1", "field"),
        ("noah.fontaine@etu.univ-amu.fr", "Fiche HTML sémantique", "Développement web", "Fiche", "Résumé sur les balises sémantiques HTML5.", "fiche_html_semantique.pdf", "L1", "field"),
        ("mael.andre@etu.univ-amu.fr", "TD algorithmique Python débutant", "Algorithmique", "TD", "Série d’exercices pour apprendre la logique algorithmique.", "td_algo_python_debutant.pdf", "L1", "field"),

        ("sofia.garnier@etu.univ-amu.fr", "TP Flask formulaires", "Flask", "TP", "TP sur la gestion des formulaires avec Flask.", "tp_flask_formulaires.pdf", "L2", "field"),
        ("ilyes.chevalier@etu.univ-amu.fr", "Résumé SQLite relations", "Base de données", "Fiche", "Fiche de cours sur clés primaires, étrangères et relations.", "resume_sqlite_relations.pdf", "L2", "field"),
        ("lea.francois@etu.univ-amu.fr", "TD requêtes SQL de base", "Base de données", "TD", "Exercices SELECT, INSERT, UPDATE et DELETE.", "td_requetes_sql_base.pdf", "L2", "field"),
        ("adam.leclerc@etu.univ-amu.fr", "TP authentification Flask simple", "Authentification", "TP", "Création d’un login/logout avec session.", "tp_auth_flask_simple.pdf", "L2", "field"),
        ("aya.mercier@etu.univ-amu.fr", "Fiche CSS responsive", "Développement web", "Fiche", "Résumé sur media queries et responsive design.", "fiche_css_responsive.pdf", "L2", "field"),
        ("rayan.blanc@etu.univ-amu.fr", "Examen blanc bases de données L2", "Base de données", "Examen", "Sujet type pour réviser les bases de données relationnelles.", "examen_blanc_bdd_l2.pdf", "L2", "field"),
        ("mila.henry@etu.univ-amu.fr", "TP système de favoris Flask", "Développement web", "TP", "Implémentation d’un système de favoris pour des questions ou ressources.", "tp_favoris_flask.pdf", "L2", "field"),

        ("amine.renaud@etu.univ-amu.fr", "Guide pagination Flask SQL", "Flask", "Fiche", "Méthode simple pour paginer une liste avec LIMIT et OFFSET.", "guide_pagination_flask_sql.pdf", "L3", "field"),
        ("salome.giraud@etu.univ-amu.fr", "TD hash et sécurité web", "Sécurité", "TD", "Exercices autour du hashage des mots de passe et sécurité de base.", "td_hash_securite_web.pdf", "L3", "field"),
        ("bilal.perrin@etu.univ-amu.fr", "TP upload de fichiers Flask", "Flask", "TP", "Manipulation de fichiers uploadés dans une application Flask.", "tp_upload_fichiers_flask.pdf", "L3", "field"),
        ("jade.masson@etu.univ-amu.fr", "Résumé recherche multicritère SQL", "Base de données", "Fiche", "Fiche sur les filtres combinés, LIKE et tri des résultats.", "resume_recherche_multicritere_sql.pdf", "L3", "field"),
        ("iris.marchand@etu.univ-amu.fr", "Examen blanc développement web avancé", "Développement web", "Examen", "Sujet de révision pour projet web de fin de licence.", "examen_blanc_web_avance.pdf", "L3", "field"),

        ("sami.barbier@etu.univ-amu.fr", "TP création API Flask JSON", "API", "TP", "TP sur la création d’API simples renvoyant du JSON.", "tp_api_flask_json.pdf", "M1", "field"),
        ("eva.colin@etu.univ-amu.fr", "Fiche middleware et protection des routes", "Authentification", "Fiche", "Résumé sur les contrôles d’accès aux routes.", "fiche_protection_routes.pdf", "M1", "field"),
        ("nassim.brun@etu.univ-amu.fr", "TD filtres et recherche avancée", "Développement web", "TD", "Exercices sur les filtres combinés dans une interface web.", "td_filtres_recherche_avancee.pdf", "M1", "field"),
        ("manon.paris@etu.univ-amu.fr", "Guide pages erreurs personnalisées Flask", "Flask", "Fiche", "Création de pages 404 et 500 personnalisées.", "guide_erreurs_flask.pdf", "M1", "field"),

        ("walid.picard@etu.univ-amu.fr", "Checklist déploiement application Flask", "DevOps", "Fiche", "Liste des vérifications avant déploiement d’une application Flask.", "checklist_deploiement_flask.pdf", "M2", "all"),
        ("louna.fabre@etu.univ-amu.fr", "TD optimisation SQLite", "Base de données", "TD", "Optimisation de requêtes SQLite sur base volumineuse.", "td_optimisation_sqlite.pdf", "M2", "all"),
        ("kylian.aubry@etu.univ-amu.fr", "Architecture backend plateforme étudiante", "Architecture logicielle", "Fiche", "Proposition d’architecture pour forum, ressources, profils et favoris.", "architecture_backend_plateforme_etudiante.pdf", "M2", "all"),
        ("sarah.noel@etu.univ-amu.fr", "TP intégration frontend statique Flask", "Développement web", "TP", "Connexion d’un frontend HTML/CSS statique à un backend Flask.", "tp_integration_front_flask.pdf", "M2", "field"),

        # Autres filières
        ("camille.schmitt@etu.univ-amu.fr", "TD polynômes et équations", "Mathématiques", "TD", "Exercices corrigés sur les polynômes et équations du second degré.", "td_polynomes_equations.pdf", "L1", "all"),
        ("thibault.boyer@etu.univ-amu.fr", "Fiche étude de fonctions", "Mathématiques", "Fiche", "Résumé de méthode pour étudier une fonction.", "fiche_etude_fonctions.pdf", "L2", "all"),
        ("meryem.arnaud@etu.univ-amu.fr", "Examen blanc suites numériques", "Mathématiques", "Examen", "Sujet d’entraînement sur les suites.", "examen_blanc_suites_numeriques.pdf", "L3", "all"),
        ("kenza.lemoine@etu.univ-amu.fr", "TD lois de Newton", "Physique", "TD", "Exercices d’application sur les lois de Newton.", "td_lois_newton.pdf", "L1", "all"),
        ("thomas.menard@etu.univ-amu.fr", "Fiche énergie et travail", "Physique", "Fiche", "Résumé de cours sur l’énergie cinétique et le travail.", "fiche_energie_travail.pdf", "L2", "all"),
        ("nina.dupuis@etu.univ-amu.fr", "Méthode de révision mécanique", "Physique", "Fiche", "Conseils de révision pour la mécanique.", "methode_revision_mecanique.pdf", "L3", "all"),
        ("yacine.legrand@etu.univ-amu.fr", "TD réactions chimiques", "Chimie", "TD", "Exercices pour équilibrer des réactions chimiques.", "td_reactions_chimiques.pdf", "L1", "all"),
        ("alicia.navarro@etu.univ-amu.fr", "Fiche réactions acido-basiques", "Chimie", "Fiche", "Résumé clair sur les réactions acido-basiques.", "fiche_reactions_acido_basiques.pdf", "L2", "all"),
        ("mehdi.bourgeois@etu.univ-amu.fr", "Méthode fiches anatomie", "Médecine", "Fiche", "Organisation et mémorisation des fiches d’anatomie.", "methode_fiches_anatomie.pdf", "L2", "all"),
        ("imane.gauthier@etu.univ-amu.fr", "Organisation révisions médecine", "Médecine", "Fiche", "Planning de révision et organisation des modules.", "organisation_revisions_medecine.pdf", "M1", "all"),
    ]

    for email, title, subject, resource_type, description, file_path, target_year, target_scope in resources:
        user_id = user_map[email]
        cursor.execute("""
            INSERT INTO resources (user_id, title, subject, resource_type, description, file_path, target_year, target_scope)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, title, subject, resource_type, description, file_path, target_year, target_scope))

    cursor.execute("SELECT id, title FROM resources")
    resource_map = {row["title"]: row["id"] for row in cursor.fetchall()}

    # =========================
    # 5) FAVORIS QUESTIONS
    # =========================
    favorite_questions = [
        ("graziella.samey@etu.univ-amu.fr", "Comment utiliser render_template avec Flask ?"),
        ("graziella.samey@etu.univ-amu.fr", "Comment créer une session utilisateur après connexion ?"),
        ("graziella.samey@etu.univ-amu.fr", "Pourquoi mes fichiers CSS ne se chargent pas avec Flask ?"),
        ("graziella.samey@etu.univ-amu.fr", "Comment faire une relation entre users et questions en SQLite ?"),
        ("graziella.samey@etu.univ-amu.fr", "Comment envoyer un fichier uploadé dans un dossier uploads ?"),

        ("alex.durand@etu.univ-amu.fr", "Comment faire une pagination sur une liste de questions Flask ?"),
        ("lucas.bernard@etu.univ-amu.fr", "Comment sécuriser les mots de passe avec Werkzeug ?"),
        ("emma.petit@etu.univ-amu.fr", "Comment créer une API JSON avec Flask ?"),
        ("jean.dupont@etu.univ-amu.fr", "Pourquoi utiliser url_for en Flask ?"),
        ("hugo.robert@etu.univ-amu.fr", "Comment protéger une route pour les utilisateurs connectés uniquement ?"),
    ]

    for email, question_title in favorite_questions:
        user_id = user_map.get(email)
        question_id = question_map.get(question_title)
        if user_id and question_id:
            cursor.execute("""
                INSERT OR IGNORE INTO favorite_questions (user_id, question_id)
                VALUES (?, ?)
            """, (user_id, question_id))

    # =========================
    # 6) FAVORIS RESSOURCES
    # =========================
    favorite_resources = [
        ("graziella.samey@etu.univ-amu.fr", "Guide complet environnement virtuel Python"),
        ("graziella.samey@etu.univ-amu.fr", "TP Flask formulaires"),
        ("graziella.samey@etu.univ-amu.fr", "Résumé SQLite relations"),
        ("graziella.samey@etu.univ-amu.fr", "TP système de favoris Flask"),
        ("graziella.samey@etu.univ-amu.fr", "TP intégration frontend statique Flask"),

        ("alex.durand@etu.univ-amu.fr", "Checklist déploiement application Flask"),
        ("lucas.bernard@etu.univ-amu.fr", "TD requêtes SQL de base"),
        ("emma.petit@etu.univ-amu.fr", "Guide pages erreurs personnalisées Flask"),
        ("jean.dupont@etu.univ-amu.fr", "Fiche HTML sémantique"),
        ("hugo.robert@etu.univ-amu.fr", "Architecture backend plateforme étudiante"),
    ]

    for email, resource_title in favorite_resources:
        user_id = user_map.get(email)
        resource_id = resource_map.get(resource_title)
        if user_id and resource_id:
            cursor.execute("""
                INSERT OR IGNORE INTO favorite_resources (user_id, resource_id)
                VALUES (?, ?)
            """, (user_id, resource_id))

    conn.commit()
    conn.close()
    print("✅ Données supplémentaires volumineuses ajoutées avec succès.")


if __name__ == "__main__":
    seed_extra()