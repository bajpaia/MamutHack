from flask import *
import pandas as pd
import numpy as np
import pickle
from qqqueue import Client
app = Flask(__name__)

DB = pd.read_csv('./data/cardio_train.csv')
MODEL_PATH = './models/XGBC_cardiac.pickle'
MODEL = pickle.load(open(MODEL_PATH, 'rb'))
QUEUE = []
CLIENT = 0

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<selection>')
def assesment(selection):
    if selection == 'sign_up':
        return redirect(url_for('sign_up'))
    else:
        return redirect(url_for('sign_in'))


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')

    idx = len(DB) + 1
    age = request.form['age']
    gender = request.form['gender']
    height = request.form['height']
    weight = request.form['weight']
    ap_hi = request.form['ap_hi']
    ap_lo = request.form['ap_low']
    chol = request.form['chol']
    gluc = request.form['gluc']
    smoke = request.form['smoke']
    alc = request.form['alc']
    active = request.form['active']
    new_data = pd.DataFrame([{'height': int(height), 'weight': int(weight), 'ap_hi': int(ap_hi), 'ap_lo': int(ap_lo),
                              'cholesterol': int(chol), 'gluc': int(gluc), 'smoke': int(smoke), 'alco': int(alc)}])
    risk = MODEL.predict_proba(new_data)
    new_db = DB.append(
        pd.DataFrame([{'height': int(height), 'weight': int(weight), 'ap_hi': int(ap_hi), 'ap_lo': int(ap_lo),
                       'cholesterol': int(chol), 'gluc': int(gluc), 'smoke': int(smoke), 'alco': int(alc),
                       'active': int(active), 'age': int(age), 'gender': int(gender)}]))
    new_db.to_csv('./data/cardio_train.csv', index=False)
    return "Thank you, wait for your ID: {0} to be shown on the screen, risk = {1}".format(idx, risk[0][1])


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    global QUEUE
    if request.method == 'GET':
        return render_template('sign_in.html')
    idx = int(request.form['ID'])
    data = DB[DB['id'] == idx]
    data = data.drop(["cardio", 'age', 'gender', 'id', 'active'], axis=1)
    data = data[['height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco']]
    risk = MODEL.predict_proba(data)
    QUEUE.append(Client(idx, risk[0][1]))
    QUEUE = sorted(QUEUE, key=lambda x: x.get_priority(), reverse=True)
    return f"Thank you, wait for your ID: {idx} to be shown on the screen"

@app.route('/queue')
def queue():
    content = '<br>'.join([f"{x.id}, {x.risk}" for x in QUEUE])
    return render_template('queueee.html', content=content)

@app.route('/display')
def disp():
    global CLIENT
    nid = QUEUE[CLIENT].id
    CLIENT += 1
    return f'<h1>{nid}</h1>'