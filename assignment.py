from flask import Flask,jsonify,render_template,request
from datetime import datetime, timedelta
from pymongo import MongoClient
import json

app=Flask(__name__)

url="mongodb://localhost:27017"

database_name = "Assessment"
collection_name = "SaleData"
collection_name1="data"
client = MongoClient(url)

collection = client[database_name][collection_name]
collection1= client[database_name][collection_name1]


average_sales=list(collection.find())
budget_data=list(collection1.find())

def load_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"sales": {"data": []}}
    
    
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file)
        

                       
@app.route('/api/id/<int:id>')
def calculateweaklydata(id):
    for i in range(len(budget_data)-1):
        sales_data = load_data()
        sales_data["sales"]["data"] = []
        if budget_data[i+1]['Week']==id:
            for j in average_sales:
                
                budgetFactor = (budget_data[i+1]['Budget'])/(budget_data[i]['Budget'])
                Quantity = j['AvgSales'] * 7 * budgetFactor
                
                
                new_sale= {
                'Article': j['Article'],
                'Week_no': budget_data[i+1]['Week'],
                'Quantity': Quantity
                }
                sales_data["sales"]["data"].append(new_sale)

                save_data(sales_data)
                
            return load_data()["sales"]["data"]
        
@app.route('/api/getall')
def calculateweaklydata1():
    sales_data = load_data()
    sales_data["sales"]["data"] = []
    for i in range(len(budget_data)-1):
        for j in average_sales:
                
            budgetFactor = (budget_data[i+1]['Budget'])/(budget_data[i]['Budget'])
            Quantity = j['AvgSales'] * 7 * budgetFactor
                
                
            new_sale= {
                'Article': j['Article'],
                'Week_no': budget_data[i+1]['Week'],
                'Quantity': Quantity
                }
            sales_data["sales"]["data"].append(new_sale)

            save_data(sales_data)
                
    return load_data()["sales"]["data"]
        
@app.route("/")
def home():
    return render_template('index.html')

@app.route('/getdata',methods=['GET','POST'])
def getdata():
    id=request.form.get("id")
    print(id)
    
    import requests

    url = f"http://127.0.0.1:5000/api/id/{id}"
    response = requests.get(url)

    if response.status_code == 200:
        print("Response content:")
        data=(response.json())
        print(data)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

    return render_template('index.html',data=data)
app.run(debug=True)