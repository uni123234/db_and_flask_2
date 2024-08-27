import logging

from flask import Blueprint, render_template, request, redirect

from app.db import add_question, get_questions

bp = Blueprint("tests", __name__)

filename = "data.txt"


@bp.route("/")
def root():
    poll_data = get_questions()
    poll_data = [dict(row) for row in poll_data]
    return render_template("poll.html", data=poll_data, number_of_ques=len(poll_data))


@bp.route("/add_test", methods=["GET", "POST"])
def add_test():
    if request.method == "GET":
        return render_template("add_test.html")
    else:
        number_of_ques = int(request.form.get("numberOfQuestions"))
        for number in range(1, number_of_ques+1):
            question = request.form.get(f"question{number}")
            answers = request.form.get(f"answers{number}")
            correct = request.form.get(f"correct{number}")
            add_question(question, answers, correct)
        return redirect("/")


@bp.route("/poll")
def poll():
    vote = request.args.get('vote')
    if not vote:
        return "No vote submitted", 400

    number_of_ques = int(request.args.get('numberOfQues'))

    correct_answers = 0

    for i in range(1, number_of_ques+1):
        question = request.args.get(f"question_{i}")
        answers = request.args.get(f"answers_{i}").split(',')
        correct = request.args.get(f"correct_{i}")

        if correct in answers:
            correct_answers += 1

    return f"You got {correct_answers}/{number_of_ques} correct answers."
