"""
Routes for handling test-related operations.

This module defines routes for:
- Displaying the test questions
- Adding new tests
- Submitting and processing test results
"""

import logging
from flask import Blueprint, render_template, request, redirect
from app.db import add_question, get_questions

bp = Blueprint("tests", __name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@bp.route("/")
def root():
    """
    Display the list of test questions.

    Retrieves questions from the database and renders them in the 'poll.html' template.

    Returns:
        str: Rendered HTML template with test questions and the number of questions.
    """
    logger.info("Fetching test questions from the database.")
    poll_data = get_questions()
    poll_data = [dict(row) for row in poll_data]
    logger.info("Fetched %d questions.", len(poll_data))
    return render_template("poll.html", data=poll_data, number_of_ques=len(poll_data))


@bp.route("/add_test", methods=["GET", "POST"])
def add_test():
    """
    Handle the addition of new test questions.

    - For GET requests, renders the form for adding new test questions.
    - For POST requests, processes the form data to add new questions
      to the database and then redirects to the root route.

    Returns:
        str: Rendered template for GET requests or a redirect response for POST requests.
    """
    if request.method == "GET":
        logger.info("Rendering form to add new test questions.")
        return render_template("add_test.html")
    else:
        number_of_ques = int(request.form.get("numberOfQuestions", 0))
        logger.info("Adding %d new test questions.", number_of_ques)
        try:
            for number in range(1, number_of_ques + 1):
                question = request.form.get(f"question{number}")
                answers = request.form.get(f"answers{number}")
                correct = request.form.get(f"correct{number}")
                add_question(question, answers, correct)
                logger.info(
                    "Added question: %s, Answers: %s, Correct: %s",
                    question,
                    answers,
                    correct,
                )
            return redirect("/")
        except ValueError as e:
            logger.error("ValueError while processing form data: %s", e)
            return "Invalid data provided", 400
        except KeyError as e:
            logger.error("KeyError while processing form data: %s", e)
            return "Missing data in form", 400


@bp.route("/poll")
def poll():
    """
    Process poll submissions and return the number of correct answers.

    Retrieves answers submitted by the user and compares them with the correct answers.
    Returns a message indicating the number of correct answers.

    Returns:
        str: Message with the number of correct answers out of the total number of questions.
    """
    vote = request.args.get("vote")
    if not vote:
        logger.warning("No vote submitted.")
        return "No vote submitted", 400

    number_of_ques = int(request.args.get("numberOfQues", 0))
    correct_answers = 0

    logger.info("Processing poll for %d questions.", number_of_ques)
    try:
        for i in range(1, number_of_ques + 1):
            answers = request.args.get(f"answers_{i}").split(",")
            correct = request.args.get(f"correct_{i}")

            if correct in answers:
                correct_answers += 1

        result_message = f"You got {correct_answers}/{number_of_ques} correct answers."
        logger.info(result_message)
        return result_message
    except KeyError as e:
        logger.error("KeyError in poll processing: %s", e)
        return "Error processing poll", 400
    except ValueError as e:
        logger.error("ValueError in poll processing: %s", e)
        return "Invalid data in poll", 400
