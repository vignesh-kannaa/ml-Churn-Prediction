from flask import Flask, request, render_template
import os
import pickle
import pandas as pd

application = Flask(__name__)
app = application


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictData', methods=['POST'])
def predictData():
    formData = request.get_json()
    features = form_data(formData)
    model, preprocessor = loadModel()
    transformed_data = preprocessor.transform(features)
    results = model.predict(transformed_data)
    result = 'Customer will Stay!' if results[0] == 0 else 'Customer may Leave!!!<br/>Take necessary steps'
    img = 'thumbs_up.gif' if results[0] == 0 else 'thumbs_down.gif'
    return [result, img]


@app.route('/predictBulkData', methods=['POST'])
def predictBulkData():
    bulkfile = request.files['bulkuploadfile']
    if bulkfile:
        model, preprocessor = loadModel()
        fileContentdata = pd.read_csv(bulkfile)
        transformed_data = preprocessor.transform(fileContentdata)
        predictions = model.predict(transformed_data)
        print(predictions)
        results = formatBulkResult(fileContentdata, predictions)
        print(results)
        return results
    else:
        return 'No data found!'


def loadModel():
    model_path = os.path.join("notebook/pickle", "model.pkl")
    preprocessor_path = os.path.join('notebook/pickle', 'preprocessor.pkl')
    preprocessor = load_object(file_path=preprocessor_path)
    model = load_object(file_path=model_path)
    return model, preprocessor


def form_data(formdata):
    data = {
        "customerName": formdata['customerName'],
        "country": formdata['country'],
        "gender": formdata['gender'],
        "age": formdata['age'],
        "tenure": formdata['tenure'],
        "balance": formdata['balance'],
        "credit_score": formdata['creditScore'],
        "products_number": formdata['productsNumber'],
        "credit_card": formdata['creditCard'],
        "active_member": formdata['activemember'],
        "estimated_salary": formdata['estimatedSalary'],
    }
    features = pd.DataFrame([data])
    return features


def load_object(file_path):
    with open(file_path, "rb") as file_obj:
        return pickle.load(file_obj)


def formatBulkResult(fileContentdata, modelPredictions):
    results = ''
    for customer, prediction in zip(fileContentdata['customer_name'], modelPredictions):
        results += customer+' - ' + \
            ('Churn' if prediction == 1 else 'No Churn') + '<br/>'
    return results


if __name__ == "__main__":
    app.run(host="0.0.0.0")
