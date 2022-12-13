# This file can also fe served from waitress-serve --listen 192.168.31.26:8080 Flask_App:app

import os
import pickle, json
import pandas as pd
from flask import Flask,request,jsonify
import configparser
from data_transform import *

config = configparser.ConfigParser()


config.read(r'../Config/config.ini')

model_file = r'../Model/finalized_model.sav'

with open(model_file, 'rb') as f_in:
    model = pickle.load(f_in)
    
app = Flask('Credit')

################################################################################### 
#                         Prediction using Internal requests library              #  
###################################################################################

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ip = request.get_json()
    data = pd.DataFrame(ip,index=range(1))
    data = dataPreparation(data)
    
    pred = model.predict(data)
    
    if pred[0] == 0:
        res = 'The user is not going to be default and will continue the service'
    else:
        res = 'There is high chance customer is going to default in near future'
    
    result = {
                'Result' : res
             }
    return jsonify(result)

################################################################################### 
#                         Prediction using web form                               #  
###################################################################################

# @app.route('/predict_form', methods=['POST'])
# def predict_form():
#     rvul = request.form.get('RevolvingUtilizationOfUnsecuredLines')
#     wds = request.form.get('Weighted_Delay_sum')
#     age_cat = request.form.get('age_cat')
#     income = request.form.get('MonthlyIncome')
#     db = request.form.get('DebtRatio')
#     dep = request.form.get('NumberOfDependentsTR')
#     nrl = request.form.get('NumberRealEstateLoansOrLinesTR')
#     nocl = request.form.get('NumberOfOpenCreditLinesAndLoansTR')
    
#     col_names = ['RevolvingUtilizationOfUnsecuredLines', 'Weighted_Delay_sum', 'age_cat',
#        'MonthlyIncome', 'DebtRatio', 'NumberOfDependentsTR',
#        'NumberRealEstateLoansOrLinesTR', 'NumberOfOpenCreditLinesAndLoansTR']
    
#     input_query = np.array([[rvul,wds,age_cat,income,db,dep,nrl,nocl]])
    
#     data = pd.DataFrame(input_query,columns = col_names)
    
#     pred = model.predict(data)
    
#     if pred[0] == 0:
#         res = 'The user is not going to be default and will continue the service'
#     else:
#         res = 'There is high chance customer is going to default in near future'
    
#     result = {
#                 'Result' : res
#              }
#     return jsonify(result)

################################################################################### 
#                         Prediction using web form (Modified version)            #  
###################################################################################

@app.route('/predict_form', methods=['POST'])
def predict_form():
    
    rvul = float(request.form.get('RevolvingUtilizationOfUnsecuredLines'))

    delay30 = int(request.form.get('NumberOfTime30-59DaysPastDueNotWorse'))
    delay60 = int(request.form.get('NumberOfTime60-89DaysPastDueNotWorse'))
    delay90 = int(request.form.get('NumberOfTimes90DaysLate'))
    
    age = int(request.form.get('age'))
    
    income = float(request.form.get('MonthlyIncome'))
    db = float(request.form.get('DebtRatio'))
    
    dep = int(request.form.get('NumberOfDependents'))
    nrl = int(request.form.get('NumberRealEstateLoansOrLines'))
    nocl = int(request.form.get('NumberOfOpenCreditLinesAndLoans'))
    
    col_names = json.loads(config.get("Variables","var_list"))
    
    input_query = [[rvul,delay30,delay60,delay90,age,income,db,dep,nrl,nocl]]
    
    data = pd.DataFrame(input_query,columns = col_names)
        
    dc = Data_Preparation()
    data = dc.fit_transform(data)
    
    pred = model.predict(data)
    
    if pred[0] == 0:
        res = config['Output_message']['pos']
    else:
        res = config['Output_message']['neg']
    
    result = {
                'Result' : res
             }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)