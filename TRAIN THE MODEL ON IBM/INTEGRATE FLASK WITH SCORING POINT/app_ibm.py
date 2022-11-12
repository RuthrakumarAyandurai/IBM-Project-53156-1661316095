import requests
import numpy as np
from flask import Flask, redirect, url_for, render_template, request

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "ZpX-YXfeK9dPqp41dYk1ly1faNv4XM2XfYomx8pIcdZW"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/y_predict", methods=['POST']) 
def y_predict():
    int_features=[float(x) for x in request.form.values()]
    final_features=[list(int_features)]

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [int_features], "values": final_features}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/16fab11a-5a0c-4180-8216-d760800e43d3/predictions?version=2022-11-08', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring)
    predictions=response_scoring.json()
    predict = predictions['predictions'][0]['values'][0][0]   
    print("Final prediction :",predict)


    # showing the prediction results in a UI# showing the prediction results in a UI
    if predict==True:        
        return render_template("chance.html")
    else:
        return render_template("noChance.html")

if __name__=='__main__':
    app.run()
