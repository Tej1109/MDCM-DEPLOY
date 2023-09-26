import pickle
import numpy as np
from flask import Flask, request, url_for, redirect, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def Home():
    return render_template("index.html")


@app.route('/results',methods = ['GET','POST'])
def results():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        dict1 ={}
        for i in to_predict_list.keys():
            dict1[i.title()] = to_predict_list[i]
        df = pd.DataFrame(dict1, index=[0])
        df.rename(columns={'Seller_Type':'Seller Type','Max_Power':'Max Power','Max_Torque': 'Max Torque','Seating_Capacity' : 'Seating Capacity',
                   'Fuel_Tank_Capacity' : 'Fuel Tank Capacity','Fuel_Type': 'Fuel Type'},inplace=True)
        cols = ['Year', 'Kilometer', 'Engine', 'Max Power', 'Max Torque', 'Length', 'Width', 'Height', 'Seating Capacity', 'Fuel Tank Capacity']
        for i in cols:
            df[i] = df[i].astype(int)
        model = pickle.load(open('model.sav','rb'))
        pred = model.predict(df)
        return render_template('result.html',prediction = pred)

if __name__ == '__main__':
    app.run()