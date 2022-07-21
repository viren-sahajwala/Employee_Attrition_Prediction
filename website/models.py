# here we are going to add our models for execution for prediction
import pandas as pd
# import numpy as np

# for the prediction we will be using random forest 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def calc_score(emp_id):
    hr_data = pd.read_csv("hr_data.csv")  # cleaned and processed data
    X=hr_data.drop(['Attrition','Over18','EmployeeID'],axis=1).values
    y=hr_data['Attrition'].values
    X_train, X_test,y_train, y_test =train_test_split(X,y,train_size=0.8) 
    model=RandomForestClassifier()
    model.fit(X_train,y_train)
    
    # now we will filter the data and find feature values for the given employee id 
    # and then predict the probability score
    try:
        for i in hr_data["EmployeeID"]:
            if i == emp_id:
                input_variable = hr_data.loc[hr_data["EmployeeID"] == i].drop(['Attrition','Over18','EmployeeID'],axis=1)
                score = model.predict_proba(input_variable)[0][1]
                print(score)
    except ValueError:
        print("Value Error occurred")
    return score


# this will be used later in the second version to autocomplete rest of the data based on employee's id
# def check_values(emp_id, dept_name, jobrole, ):