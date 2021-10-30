import numpy as np
import pandas as pd
from joblib import load
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request

app = Flask(__name__)
n_features = 8

@app.route('/')
def home():
    return render_template("home.html", pred='1/8')

@app.route('/get_data', methods=['POST'])
def get_data():
    message = float([x for x in request.form.values()][0])
    
    f = open("data.txt", "a+")
    f.write(str(message))
    f.write("\n")
    f.close()
    
    f = open("data.txt", "r+")
    data = [r for r in f.readlines()]
    f.close()

    #if f.mode == "r":
     #   data = f.read()
    #f.close()

    """num = (len(data)%n_features)+1
    
    if num == n_features:
        model = load("model.joblib")
        data = data[-1*n_features:]
        data = np.array(data).reshape(1, -1)

        prediction = model.predict(data)[0]
        return render_template("home.html", pred=f"Food supply will be {prediction} (kcal/capita/day)", data_num='1/8')"""
    return render_template("home.html", data_num=f"{data}")

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
