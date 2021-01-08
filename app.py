from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import BadRequestKeyError

from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = '<replace with a secret key>'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

responses = []


@app.route('/start-survey')
def start_survey():
    survey_title = surveys['satisfaction'].title
    survey_instructions = surveys['satisfaction'].instructions

    return render_template(
        "start_survey.html",
        survey_title=survey_title,
        survey_instructions=survey_instructions,
    )


@app.route('/answer', methods=["POST"])
def answered_question():
    try:
        choice = request.form['survey-choice']
        responses.append(choice)
        if len(responses) == len(surveys['satisfaction'].questions):
            responses.clear()
            next_step = redirect('/finished')
        else:
            next_step = redirect(f'/question/{len(responses)}')
    except BadRequestKeyError:
        next_step = redirect(f'/question/{len(responses)}')

    return next_step


@app.route('/question/<int:index>', methods=["POST", "GET"])
def questions(index):
    if index != len(responses):
        flash(
            'You tried to access an invalid question. '
            'Please, answer the question bellow.'
        )
        return redirect(f'/question/{len(responses)}')

    survey_data = surveys['satisfaction']
    question = survey_data.questions[index].question
    choices = survey_data.questions[index].choices

    return render_template(
        "survey_questions.html",
        question=question,
        choices=choices,
        responses_list=responses,
    )


@app.route('/finished')
def finished():
    return render_template('finished.html')

