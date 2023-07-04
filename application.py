from flask import Flask, request, render_template
import os
import pickle
import pandas as pd
from flask import jsonify

application = Flask(__name__)
app = application


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    model_path = os.path.join("notebook/pickle", "model.pkl")
    preprocessor_path = os.path.join('notebook/pickle', 'preprocessor.pkl')
    preprocessor = load_object(file_path=preprocessor_path)
    model = load_object(file_path=model_path)

    if request.form.get('fileType') == 'on':
        # print('inside the bulk option')
        if 'bulkuploadfile' in request.files:
            bulkfile = request.files['bulkuploadfile']
            # print('bulkfile:', bulkfile)
            # file_content = bulkfile.read()
            # file = request.files['bulkuploadfile']
            fileContentdata = pd.read_csv(bulkfile)
            # print(fileContentdata)
            transformed_data = preprocessor.transform(fileContentdata)
            results = model.predict(transformed_data)
            html_content = convert_to_html(fileContentdata, results)
            return render_template('index.html', bulkResult=html_content)

    else:
        features = form_data()
        transformed_data = preprocessor.transform(features)
        results = model.predict(transformed_data)
        print('results:', results)
        # result = 'No Churn' if results[0] == 0 else 'Churn'
        return render_template('index.html', results=results[0])


def form_data():
    data = {
        "customerName": request.form.get('customerName'),
        "country": request.form.get('country'),
        "gender": request.form.get('gender'),
        "age": request.form.get('age'),
        "tenure": request.form.get('tenure'),
        "balance": request.form.get('balance'),
        "credit_score": request.form.get('creditScore'),
        "products_number": request.form.get('productsNumber'),
        "credit_card": request.form.get('creditCard'),
        "active_member": request.form.get('activemember'),
        "estimated_salary": request.form.get('estimatedSalary'),
    }
    # data = {
    #     "customerName": request.form['customerName'],
    #     "country": request.form['country'],
    #     "gender": request.form['gender'],
    #     "age": request.form['age'],
    #     "tenure": request.form['tenure'],
    #     "balance": request.form['balance'],
    #     "credit_score": request.form['creditScore'],
    #     "products_number": request.form['productsNumber'],
    #     "credit_card": request.form['creditCard'],
    #     "active_member": request.form['activemember'],
    #     "estimated_salary": request.form['estimatedSalary'],
    # }
    data['credit_card'] = 1 if data['credit_card'] == 'yes' else 0
    data['active_member'] = 1 if data['active_member'] == 'yes' else 0
    features = pd.DataFrame([data])
    return features


def load_object(file_path):
    with open(file_path, "rb") as file_obj:
        return pickle.load(file_obj)


def convert_to_html(fileContentdata, results):
    table_html = '''
        <div class="relative overflow-x-auto" style="width: 50%;    margin: auto; padding-top: 5%">
            <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                        <th scope="col" class="px-6 py-3">
                            Customer Name
                        </th>
                        <th scope="col" class="px-6 py-3">
                            Result
                        </th>
                    </tr>
                </thead>
                <tbody>
        '''

    for customer, result in zip(fileContentdata['customer_name'], results):
        if result == 1:
            row_class = "bg-white border-b dark:bg-gray-800 dark:border-gray-700"
            result_text = "Churn"
        else:
            row_class = "bg-white dark:bg-gray-800"
            result_text = "No Churn"
        table_html += '''
                <tr class="{}">
                    <td class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        {}
                    </td>
                    <td class="px-6 py-4">
                        {}
                    </td>
                </tr>
            '''.format(row_class, customer, result_text)

    table_html += '''
                </tbody>
            </table>
        </div>
        '''

    return table_html


if __name__ == "__main__":
    app.run(host="0.0.0.0")
