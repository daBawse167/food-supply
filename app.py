import numpy as np
import pandas as pd
from joblib import load
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request

app = Flask(__name__)
n_features = 8

@app.route('/')
def home():
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

@app.route('/box', methods=['POST'])
def box():
    url = "https://raw.githubusercontent.com/daBawse167/owid-datasets/master/datasets/Food%20supply%20(FAO%2C%202020)/Food%20supply%20(FAO%2C%202020).csv"
    df = pd.read_csv(url).drop('Food supply (kcal/capita/day) - Grand Total', axis=1)
    message = [x for x in request.form.values()][0]

    if message not in np.unique(df['Entity']):
        return f"Country is not in our list. Please go back to your browser.", 400

    model = load("model.joblib")

    avg = np.nanmean(df['Pigmeat food supply quantity (kg/capita/yr)'])
    df = df.fillna(avg)

    to_pred = (df[df["Entity"]==message]).drop('Entity', axis=1)
    prediction = round(model.predict(to_pred)[0])

    return render_template("home.html", pred=f"Food supply will be {prediction} (kcal/capita/day)")

if __name__ == "__main__":
    app.run(debug=True)
