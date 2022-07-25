from encodings import utf_8
from flask import Blueprint, render_template, request, json
from werkzeug.exceptions import HTTPException
from .models import *

from trycourier import Courier
client = Courier(auth_token="pk_prod_83ZBZW1KDMM656P29P1G7T13EKCC")

# Loading model to compare the results
#import pickle
#model = pickle.load( open('model.pkl','rb'))

# for validating if the employee id exits in the dataset
#import pandas as pd
#hr_data = pd.read_csv("hr_data.csv", encoding="utf_8")

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
def home():
    return render_template("home.html")

@views.route('/prediction',methods=['GET','POST'])
def prediction():
    emp_id = request.form.get("emp_id", False)
    emp_id = int(emp_id)
    score = calc_score(emp_id)

    if score < 0.7:
        prob_status = "Low Risk"
    elif score < 0.9:
        prob_status = "Moderate Risk"
    else:
        prob_status = "High Risk"
    
    body = "Attrition score for Employee ID: " + str(emp_id) + " is " + str(score) + "\nStatus: " + prob_status
    client.send_message(
            message={"to": { "email": "viren.sahajwala@gmail.com"}, 
            "routing": {"method": "single", "channels": ["email"]},
          "channels" : {"email": {"providers": ["gmail"] }},
          "content": {
            "title": "Employee Attribution Model Report!",
            "body": body
          },
          "data":{"n_mane": "Thankyou!"}
          })

    return render_template("output.html", emp_id = emp_id, score = score, prob_status = prob_status) 


# general HTTP Error Handling
@views.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response
