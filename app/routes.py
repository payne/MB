from flask import render_template, flash, redirect, url_for, request
import json
from app import app
from app.forms import DepositForm
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
  deposits_list = users.current.get('deposits', [])
  form = DepositForm()
  dateTimeObj = datetime.now()
  ts = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
  if form.amount.data:
    amt = form.amount.data
    deposits_list.append((f"{amt}",ts)) # replit database likes strings but not decimal.Decimal
    users.current['deposits'] = deposits_list
  return render_template('deposit.html',title='Deposit',deposit_history = deposits_list, form=form)

@app.route('/json', methods=['GET'])
@web.authenticated
def output_json():
  users = web.UserStore()
  stuff = users.current.get('stuff', [])
  deposits = users.current.get('deposits', [])
  # Loop over the stuff in the database to make plain lists that can be serialized to json
  # TODO: Start using a class for things in the database instead of tuples
  stuff_list = [ (a[0],a[1]) for a in stuff ]
  deposits_list = [ (a[0],a[1]) for a in deposits ]
  the_data = {'purchases': stuff_list, 'deposits': deposits_list}
  s = json.dumps(the_data, indent = 1)
  return f"<pre>{s}</pre>"

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
  balance=0.0
  return render_template('index.html', title='Home', stuff=stuff, balance=balance)

@app.route('/listHistory', methods=['GET', 'POST'])
@web.authenticated
def list_history():
  users = web.UserStore()
  stuff = users.current.get('stuff', [])
  deposits_list = users.current.get('deposits', [])
  return render_template('list.html', title='Home', history=stuff, deposit_history = deposits_list)

@app.route('/clear', methods=['GET', 'POST'])
@web.authenticated
def clear():
  users = web.UserStore()
  if 'stuff' in users.current: del users.current['stuff']
  if 'deposits' in users.current: del users.current['deposits']
  return redirect(url_for("status"))

@app.route('/', methods=['GET', 'POST'])
def about():
  return render_template('about.html')

@app.route('/eg', methods=['GET', 'POST'])
def example():
  return render_template('example.html')
