import os
import numpy as np
import pandas as pd
from joblib import load
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request

app = Flask(__name__)
n_features = 8

@app.route('/')
def home():
    if os.path.isdir("./data.txt"):
        f = open("data.txt", "r+")
        f.truncate(0)
        f.close()
    return render_template("home.html", pred='1/8')

@app.route('/get_data', methods=['POST'])
def get_data():
    message = float([x for x in request.form.values()][0])
    
    f = open("data.txt", "a+")
    f.write(str(message)+'\n')
    f.close()
    
    f = open("data.txt", "r+")
    data = [float(r[:-2]) for r in f.readlines()]
    f.close()

    length = len(data)
    if length >= 8:
        model = load("model.joblib")
        data = np.array(data).reshape(1, -1)
        prediction = model.predict(data)[0]
        
        f = open("data.txt", "r+")
        f.truncate(0)
        f.close()
        return render_template("home.html", pred=f"Food supply will be {prediction} (kcal/capita/day)", data_num='1/8')
    return render_template("home.html", data_num=f"{length+1}/{n_features}")

if __name__ == "__main__":
    app.run(debug=True)
