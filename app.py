from flask import *
import pandas as pd
import pickle

app = Flask(__name__)


DB = pd.read_csv('./data/cardio_train.csv')
MODEL_PATH = './models/XGBC_cardiac.pickle'
MODEL = pickle.load(open(MODEL_PATH, 'rb'))

@app.route('/')
def home():
   return render_template('index.html')


# @app.route('/<selection>')
# def assesment(selection):
#     if selection == 'sign_up':
#         return redirect(url_for('sign_up'))
#     else:
#        return redirect(url_for('sign_in'))


@app.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    if request.method =='GET':
        return render_template('sign_up.html')
    print(DB.head())
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
    alc =  request.form['alc']
    active =  request.form['active']
    row = [idx, age, gender, height, weight, ap_hi, ap_lo, chol, gluc, smoke, alc, active]
    DB.loc[len(DB)] = row
    risk = MODEL.predict_proba(DB.loc[idx])
    return "Thank you, wait for your ID: {0} to be shown on the screen, risk = {1}".format(idx, risk)
    

@app.route('/sign_in')
def sign_in(methods = ['GET', 'POST']):
    if request.method == 'GET':
        return render_template('sign_in.html')
    
    