from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from app.forms import ConsumeForm
from replit import db, web


@app.route('/', methods=['GET', 'POST'])
@web.authenticated
def index():
  form = ConsumeForm()
  users = web.UserStore()
  stuff = users.current.get('stuff', [])
  if form.thing.data:
    for x in form.thing.data:
      stuff.append(x)
  users.current['stuff'] = stuff
  return render_template('index.html', title='Home', stuff=stuff, form=form)

@app.route('/clear', methods=['GET', 'POST'])
@web.authenticated
def clear():
  users = web.UserStore()
  del users.current['stuff']
  return f"<h2>database for {web.auth.name} has its 'stuff' key removed.</h2>"

@app.route('/eg', methods=['GET', 'POST'])
def example():
  return render_template('example.html')
