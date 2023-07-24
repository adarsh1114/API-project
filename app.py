from flask import Flask,render_template,request,redirect,url_for, jsonify


import pandas as pd
import os
import mysql
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


app.config['DEBUG'] = True

UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import mysql.connector

conn = mysql.connector.connect(
user='root', password='', host='localhost', database='exceldb'
)

cursor = conn.cursor()

@app.route('/',methods=['POST'])
def uploadFiles():
    uploaded_file = request.files['file']
    
    if uploaded_file.filename!='':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],uploaded_file.filename)
        uploaded_file.save(file_path)
        parseCSV(file_path)

    return redirect(url_for("index"))

def parseCSV(filePath):
    col_names = ['datetime','close','high','low','open','vol','instrument']

    csvData = pd.read_csv(filePath,names=col_names,header=None)

    for i, row in csvData.iterrows():
        sql = "INSERT INTO users (datetime,close,high,low,open,vol,instrument) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        value = (row['datetime'],row['close'],row['high'],row['low'],row['open'],row['vol'],row['instrument'])
        cursor.execute(sql,value)
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_data', methods=['GET'])
def get_data():
    table_name = "users"
    query = f"SELECT datetime, close, high, low, open, vol, instrument FROM `{table_name}`"
    cursor.execute(query)
    data = cursor.fetchall()

    # Converting the data to a list of dictionaries
    data_list = [{'datetime': item[0], 'close': item[1],'high':item[2],'low':item[3],'open':item[4],'vol':item[5],'instrument':item[6]} for item in data]

    return jsonify(data_list)

if __name__ == "__main__":
    app.run(port=5000)