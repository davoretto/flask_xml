#!/usr/bin/env python

from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import Form
from wtforms.fields import RadioField, StringField, SubmitField
from wtforms.validators import Required
from guess import Guess, GuessError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
game = Guess('Python')
game.expand('Python', 'C++', 'Is it interpreted?', False)
game.expand('C++', 'Java', 'Does it run on a VM?', True)


class YesNoQuestionForm(Form):
    answer = RadioField('Your answer', choices=[('yes', 'Yes'), ('no', 'No')])
    submit = SubmitField('Submit')


class LearnForm(Form):
    language = StringField('What language did you pick?',
                           validators=[Required()])
    question = StringField('What is a question that differentiates your '
                           'language from mine?', validators=[Required()])
    answer = RadioField('What is the answer for your language?',
                        choices=[('yes', 'Yes'), ('no', 'No')])
    submit = SubmitField('Submit')


class LoadRecipeForm(Form):
    session_name = StringField('Name for this session',
                           validators=[Required()])

    submit = SubmitField('Submit')


@app.route('/')
def index():
    session['question'] = 0
    return render_template('index.html')


@app.route('/learn', methods=['GET', 'POST'])
def learn():
    if 'question' not in session:
        # if we have no question in the session we go to the start page
        return redirect(url_for('index'))

    id = session['question']
    guess = game.get_guess(id)
    if guess is None:
        # we don't have a guess, we shouldn't be here
        return redirect(url_for('index'))

    form = LearnForm()
    if form.validate_on_submit():
        game.expand(guess, form.language.data, form.question.data,
                    form.answer.data == 'yes')
        return redirect(url_for('index'))
    return render_template('learn.html', guess=guess, form=form)


@app.route('/load', methods=['GET', 'POST'])
def load():
    if 'question' not in session:
        # if we have no question in the session we go to the start page
        return redirect(url_for('index'))

    id = session['question']
    guess = game.get_guess(id)
    if guess is None:
        # we don't have a guess, we shouldn't be here
        return redirect(url_for('index'))

    form = LearnForm()
    if form.validate_on_submit():
        game.expand(guess, form.language.data, form.question.data,
                    form.answer.data == 'yes')
        return redirect(url_for('index'))
    return render_template('learn.html', guess=guess, form=form)

@app.errorhandler(GuessError)
@app.errorhandler(404)
def runtime_error(e):
    return render_template('error.html', error=str(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
