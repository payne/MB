from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from app.forms import ConsumeForm, DepositForm
from replit import db, web
# https://replit-py.readthedocs.io/en/latest/
from datetime import datetime
from collections import Counter

prices = { 'coke': 0.5, 'celsius': 0.9, 'candy': 0.25}

@app.route('/eat', methods=['GET', 'POST'])
@web.authenticated
def eat():
  x = request.args.get('x')
  users = web.UserStore()
  stuff = users.current.get('stuff', [])
  dateTimeObj = datetime.now()
  ts = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
  stuff.append((x, ts))
  users.current['stuff'] = stuff
  return redirect(url_for("status"))
  
@app.route('/deposit', methods=['GET', 'POST'])
@web.authenticated
def deposit():
  users = web.UserStore()
  deposits = users.current.get('deposits', [])
  form = DepositForm()
  dateTimeObj = datetime.now()
  ts = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
  if form.amount.data:
    deposits.append((form.amount.data,ts))
    users.current['deposits'] = deposits
  return render_template('deposit.html',title='Deposit',deposits = deposits, form=form)


@app.route('/status', methods=['GET', 'POST'])
@web.authenticated
def status():
  users = web.UserStore()
  stuff = users.current.get('stuff', [])
  # TODO(MGP): Total up the stuff so a summary can be created
  items = [ t[0] for t in stuff ] # Remove time stamps
  c = Counter(items)
  stuff = { thing:count  for thing, count in c.most_common() }
  for thing in prices.keys():
    if (thing not in stuff):
      stuff[thing]=0
  
  return render_template('index.html', title='Home', stuff=stuff)

@app.route('/listHistory', methods=['GET', 'POST'])
@web.authenticated
def list_history():
  users = web.UserStore()
  stuff = users.current.get('stuff', [])
  return render_template('list.html', title='Home', history=stuff)

@app.route('/clear', methods=['GET', 'POST'])
@web.authenticated
def clear():
  users = web.UserStore()
  del users.current['stuff']
  return redirect(url_for("status"))

@app.route('/', methods=['GET', 'POST'])
def about():
  return render_template('about.html')

@app.route('/eg', methods=['GET', 'POST'])
def example():
  return render_template('example.html')
