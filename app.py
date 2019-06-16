import os
import pyodbc
import pandas as pd
from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)
port = int(os.getenv('VCAP_APP_PORT','5000'))

server = 'charan.database.windows.net'
database = 'charan'
username = 'charan123'
password = 'Smokescreen@5'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)


@app.route('/')
def home():
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM all_month")
    row = cursor.fetchone()
    while row:
        print(str(row[0]) + " " + str(row[1]))
        row = cursor.fetchone()
    return render_template('home.html',data = row)

@app.route('/enternew')
def upload_csv():
   return render_template('upload.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
       con = sql.connect("https://github.com/Ragav-Charan/Assignment3/database.db")
       csv = request.files['myfile']
       file = pd.read_csv(csv)
       file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)
       con.close()
   return render_template("result.html",msg = "Record inserted successfully")

@app.route('/list')
def list():
   con = sql.connect("database.db")
   cur = con.cursor()
   cur.execute("select * from Earthquake")
   rows = cur.fetchall();
   con.close()
   return render_template("list.html",data1 = rows)

if __name__ == '__main__':
    #app.run(default=True)
    app.run(host='0.0.0.0',port=port)
