from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from models.question_model import (
    create_question,
    get_question_by_id,
    get_recent_questions,
    get_user_questions,
    delete_question
)
from models.answer_model import get_answers_by_question, create_answer

question_bp = Blueprint("questions", __name__)


def get_current_user_id():
    return session.get("user_id")


@question_bp.route("/", methods=["GET"])
def list_questions():
    user_field_of_study = request.args.get("field_of_study")
    user_study_year = request.args.get("study_year")
    search = request.args.get("search")

    questions = get_recent_questions(
        user_field_of_study=user_field_of_study,
        user_study_year=user_study_year,
        search=search
    )

    return render_template("forum.html", questions=questions)


@question_bp.route("/new", methods=["GET"])
def question_form():
    user_id = get_current_user_id()
    if not user_id:
        flash("Vous devez être connecté pour poser une question.", "error")
        return redirect(url_for("auth.login"))

    return render_template("ask.html")


@question_bp.route("/", methods=["POST"])
def add_question():
    user_id = get_current_user_id()
    if not user_id:
        flash("Authentification requise.", "error")
        return redirect(url_for("auth.login"))

    title = request.form.get("title")
    subject = request.form.get("subject")
    target_year = request.form.get("target_year")
    target_scope = request.form.get("target_scope")
    description = request.form.get("description")

    if not all([title, subject, target_year, target_scope, description]):
        flash("Tous les champs sont obligatoires.", "error")
        return redirect(url_for("questions.question_form"))

    question_id = create_question(
        user_id=user_id,
        title=title,
        subject=subject,
        target_year=target_year,
        target_scope=target_scope,
        description=description
    )

    flash("Question créée avec succès.", "success")
    return redirect(url_for("questions.question_detail", question_id=question_id))


@question_bp.route("/<int:question_id>", methods=["GET"])
def question_detail(question_id):
    question = get_question_by_id(question_id)

    if not question:
        flash("Question introuvable.", "error")
        return redirect(url_for("questions.list_questions"))

    answers = get_answers_by_question(question_id)

    return render_template(
        "page-quest-rep.html",
        question=question,
        answers=answers,
        answers_count=len(answers)
    )


@question_bp.route("/<int:question_id>/answer", methods=["POST"])
def add_answer(question_id):
    user_id = get_current_user_id()
    if not user_id:
        flash("Vous devez être connecté pour répondre.", "error")
        return redirect(url_for("auth.login"))

    content = request.form.get("content")

    if not content:
        flash("La réponse ne peut pas être vide.", "error")
        return redirect(url_for("questions.question_detail", question_id=question_id))

    create_answer(question_id, user_id, content)
    flash("Réponse publiée avec succès.", "success")
    return redirect(url_for("questions.question_detail", question_id=question_id))


@question_bp.route("/my", methods=["GET"])
def my_questions():
    user_id = get_current_user_id()
    if not user_id:
        flash("Authentification requise.", "error")
        return redirect(url_for("auth.login"))

    questions = get_user_questions(user_id)
    return render_template("mes_questions.html", questions=questions)


@question_bp.route("/<int:question_id>/delete", methods=["POST"])
def remove_question(question_id):
    user_id = get_current_user_id()
    if not user_id:
        flash("Authentification requise.", "error")
        return redirect(url_for("auth.login"))

    deleted = delete_question(question_id, user_id)

    if not deleted:
        flash("Suppression impossible ou question introuvable.", "error")
    else:
        flash("Question supprimée avec succès.", "success")

    return redirect(url_for("questions.my_questions"))