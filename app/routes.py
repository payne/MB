from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from app.forms import ConsumeForm


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
  form = ConsumeForm()
  stuff = ['this','that','other']
  if form.thing.data:
    for x in form.thing.data:
      stuff.append(x)
  return render_template('index.html', title='Home', stuff=stuff, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
    return redirect(url_for('index'))
  return render_template('login.html', title='Sign In', form=form)


@app.route('/eg', methods=['GET', 'POST'])
def example():
  return render_template('example.html')
