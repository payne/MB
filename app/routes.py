from flask import render_template, flash, redirect, url_for, request
import json
from app import app
from app.forms import DepositForm
from replit import db, web
# https://replit-py.readthedocs.io/en/latest/
from datetime import datetime
from collections import Counter

prices = {
'Rice Krispy Treats': 0.21,
'candy': 0.50,
'Propel': 0.45,
'coke': 0.40, 
'celsius': 1.12
}

class Purchase:
    def __init__(self, a_thing, ts):
        self.thing = a_thing
        self.timestamp = ts

class Deposit:
    def __init__(self, an_amt, ts):
        self.amount = an_amt
        self.timestamp = ts

class MyEncoder(json.JSONEncoder):
  """
  s = json.dumps(plst, indent=2, cls=MyEncoder)
  """
  def default(self, o):
    return o.__dict__

@app.route('/eat', methods=['GET', 'POST'])
@web.authenticated
def eat():
    x = request.args.get('x')
    users = web.UserStore()
    stuff = users.current.get('stuff', [])
    dateTimeObj = datetime.now()
    ts = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    # Because of quirks of replit's db, and web can't store list objects
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
        deposits_list.append(
            (f"{amt}",
             ts))  # replit database likes strings but not decimal.Decimal
        users.current['deposits'] = deposits_list
    return render_template('deposit.html',
                           title='Deposit',
                           deposit_history=deposits_list,
                           form=form)


@app.route('/json', methods=['GET'])
@web.authenticated
def output_json():
    users = web.UserStore()
    stuff = users.current.get('stuff', [])
    deposits = users.current.get('deposits', [])
    # Loop over the stuff in the database to make plain lists that can be serialized to json
    # TODO: Start using a class for things in the database instead of tuples
    stuff_list = [Purchase(a[0], a[1]) for a in stuff]
    deposits_list = [Deposit(a[0], a[1]) for a in deposits]
    the_data = {'purchases': stuff_list, 'deposits': deposits_list}
    s = json.dumps(the_data, indent=2, cls=MyEncoder)
    return f"<pre>{s}</pre>"


@app.route('/status', methods=['GET', 'POST'])
@web.authenticated
def status():
    users = web.UserStore()
    stuff = users.current.get('stuff', [])
    # TODO(MGP): Total up the stuff so a summary can be created
    items = [t[0] for t in stuff]  # Remove time stamps
    c = Counter(items)
    stuff = {thing: count for thing, count in c.most_common()}
    for thing in prices.keys():
        if (thing not in stuff):
            stuff[thing] = 0
    deposits_list = users.current.get('deposits', [])
    balance = compute_balance(stuff, deposits_list)
    balance = "{:.2f}".format(balance)
    return render_template('index.html',
                           title='Home',
                           stuff=stuff,
                           balance=balance)


def compute_balance(purchases, deposits):
    total = 0.0
    for dt in deposits:
        total += float(dt[0])
    for thing, count in purchases.items():
        total -= float(prices[thing]) * count
    return total


@app.route('/listHistory', methods=['GET', 'POST'])
@web.authenticated
def list_history():
    users = web.UserStore()
    stuff = users.current.get('stuff', [])
    deposits_list = users.current.get('deposits', [])
    return render_template('list.html',
                           title='Home',
                           history=stuff,
                           deposit_history=deposits_list)


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
