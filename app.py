from flask import Flask, request, render_template, url_for
#import os, pymysql, pymysql.cursors, random, json
import pyodbc
import os
import time, csv
from werkzeug.utils import secure_filename
import pandas as pd
import redis
import _pickle as cPickle
import random
import json

# import redis, hashlib, datetime
# import json

app = Flask(__name__)

app.secret_key = 'your secret key'

server = 'mysqlserver-rv.database.windows.net'
username = 'azureuser'
password = 'Mavbgl@656'
database = 'demodb'
driver= '{ODBC Driver 18 for SQL Server}'

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/tmp'
print(dir_path)
UPLOAD_FOLDER = dir_path
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#redisdnsrv.redis.cache.windows.net:6380,password=ukD7wIFSxdFcJoGn8RBsP8mZ7ncNYxrdLAzCaEUbX0E=,ssl=True,abortConnect=False
#roopamdns.redis.cache.windows.net:6380,password=UKpCfgBxKqwBwPo53Rjn7HNA7kl5JJaIjAzCaEuT3pg=,ssl=True,abortConnect=False
red = redis.StrictRedis(host='roopamdns.redis.cache.windows.net',port=6380, db=0, password='UKpCfgBxKqwBwPo53Rjn7HNA7kl5JJaIjAzCaEuT3pg=', ssl=True)
#host=rds_hostname
result = red.ping()
print("Ping returned : " + str(result))

# conn = pyodbc.Connect(user=username, passwd=password, port=3306, local_infile=True, charset='utf8',
#                        cursorclass=pymysql.cursors.DictCursor)
# cursor = conn.cursor()

conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+',1433;DATABASE='+database+';UID='+username+';PWD='+ password+ ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Check Link for File Upload  http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            '<h1>Unsuccesfull</h1>'

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            '<h1>Unsuccesfull</h1>'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)


            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '<h1>Succesfull</h1>'

    return '<h1>Unsuccesfull</h1>'

@app.route('/createDB', methods=['GET'])
def createDB():
    file_name = 'tmp/all_month.csv'
    f_obj = open(file_name, 'r')
    reader = csv.reader(f_obj)
    headers = next(reader, None)
    print(headers)
    #Drop table
    drop_query = 'DROP TABLE IF EXISTS demo_data;'
    cursor.execute(drop_query)
    print("Table Dropped!!")
    # Table Create
    tablename = "demo_data"
    create_query = 'Create table ' + tablename + ' ( '
    #create_query = 'CREATE TABLE IF NOT EXISTS demo3' + ' ( '
    for heading in headers:
        create_query += heading + " varchar(100) DEFAULT NULL,"

    create_query = create_query[:-1]
    create_query += ");"
    print(create_query)
    cursor.execute(create_query)
    print('Table Created')

    # # Load Data via CSV File  
    #insert_query = """LOAD DATA LOCAL INFILE '/Users/vrastogi/Downloads/Assignment3/tmp/all_month.csv' INTO TABLE demo_data FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '/n' IGNORE 1 LINES"""
    #insert_query = """LOAD DATA LOCAL INFILE '/Users/vrastogi/Downloads/Assignment3/tmp/all_month.csv' INTO TABLE demo_data FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES"""
    db_table_nm = "demo_data"
    csv_file_nm = "roopamcontainer/all_month.csv"

    # qry = "BULK INSERT " + db_table_nm + " FROM '" + csv_file_nm + "' WITH (DATA_SOURCE = 'roopamquiz0', FORMAT = 'CSV', FIRSTROW = 2)"
    # cursor.execute(qry)

    with open ('tmp/all_month.csv', 'r') as f:
        reader = csv.reader(f)
        columns = next(reader) 
        query = 'insert into demo_data({0}) values ({1})'
        query = query.format(','.join(columns), ','.join('?' * len(columns)))
        #cursor = conn.cursor()
        #print("query: " , query)
        start_time = time.time()
        for data in reader:
            #print("data : ",data)
            cursor.execute(query, data)
            print("done")
    cursor.commit()
    end_time = time.time()

    print("TOTAL TIME TAKEN: " , end_time-start_time)
        

    # print("*******", insert_query)
    # cursor.execute(insert_query)
    # cursor.commit()
    return 'Table Created with Uploaded Schema'
    # str(result[0]['count(*)'])

@app.route('/query1', methods=['GET'])
def query1():
    query = 'SELECT count(*) FROM demo_data;'
    cursor.execute(query)
    result = cursor.fetchall()

    myquerylist = ['SELECT * from demo_data;', 'SELECT time, latitude, longitude from demo_data;', 
                   'SELECT mag from demo_data;','SELECT latitude from demo_data;','SELECT longitude from demo_data;',
                   'SELECT latitude, longitude from demo_data;',
                   'SELECT time, latitude, longitude from demo_data;',
                   'SELECT latitude, mag, longitude from demo_data;']
    
    myquery = random.randrange(0,len(myquerylist))
    start_time = time.time()

    if red.get('query1'):
        result1 = cPickle.loads(red.get('query1'+myquerylist[myquery]))
        end_time = time.time()
        time_taken = end_time-start_time
        print("returned from cache....", result1)
    else:
        start_time = time.time()
        cursor.execute(myquerylist[myquery])
        end_time = time.time()
        result1 = cursor.fetchall()
        time_taken = end_time-start_time
        red.set('query1'+myquerylist[myquery],cPickle.dumps(result1))
    #print(result)
    return render_template('query1.html', tablerows= result, tabdat = result1, myquery = myquerylist[myquery], time_taken=time_taken, query = query)

@app.route('/query2', methods=['GET'])
def query2():
    return render_template('query2.html')

# @app.route('/selectBQuery', methods=['POST'])
# def selectBQuery():
#     mag1 =request.form['mag1']
#     mag2 =request.form['mag2']
#     selected_attributes = 'mag'
#     selected_plot = request.form.getlist('chart')

#     query = "select time, latitude, longitude, mag, place from demo_data where mag >= '" + mag1 + "' and mag < '" + mag2 +"';"
#     print(query)
#     start_time = time.time()
#     chart_data = []

#     # #result = red.get('selectBQuery'+mag1+mag2)
#     # if red.get('selectBQuery'+mag1+mag2):
#     #     result = cPickle.loads(red.get('selectBQuery'+mag1+mag2))
#     #     end_time = time.time()
#     #     time_taken = end_time-start_time
#     #     print("returned from cache....", result)
#     # #cursor.execute('''SELECT time,latitude, longitude, mag, place FROM [dbo].[demo_data] where mag>='2' and mag <'5';''')
#     # else:
#     #     start_time = time.time()
#     #     cursor.execute(query)
#     #     end_time = time.time()
#     #     result = cursor.fetchall()
#     for row in result:
#         data_point = {}
#         data_point['time'] = row[0]
#         for i, attribute in enumerate(['mag']):
#             if attribute in selected_attributes:
#                 data_point[attribute] = str(row[i+1])
#         print("DATA: ",data_point)
#         chart_data.append(data_point)
#     print("CHART DATA",chart_data)

#     # Render the template with the chart data and selected attributes
#     if (selected_plot[0] == 'ScatterPlot'):
#         # time_taken = end_time-start_time
#         # print("Inside scatter....")
#         # red.set('selectBQuery'+mag1+mag2,cPickle.dumps(result))
#         return render_template('scatterplot_query2.html', chart_data=json.dumps(chart_data), selected_attributes=selected_attributes)
#     if (selected_plot[0] == 'BarChart'):
#         # time_taken = end_time-start_time
#         # print("Inside bar....")
#         # red.set('selectBQuery'+mag1+mag2,cPickle.dumps(result))
#         return render_template('histplot_query2.html', chart_data=json.dumps(chart_data), selected_attributes=selected_attributes)
#     if (selected_plot[0] == 'PieChart'):
#         # time_taken = end_time-start_time
#         # print("Inside pie....")
#         # red.set('selectBQuery'+mag1+mag2,cPickle.dumps(result))
#         return render_template('piechart_query2.html', chart_data=json.dumps(chart_data), selected_attributes=selected_attributes)
#     return render_template('retry.html')


    #return render_template('query2.html', tableData=result , time_taken = time_taken , query = query)

@app.route('/querydemo', methods=['POST'])
def querydemo():

    time1 = request.form.get('time1')
    time2 = request.form.get('time2')
    selected_attributes = 'latitude'
    selected_plot = request.form.getlist('chart')

    query = "SELECT time, latitude, mag, place FROM tableName WHERE time >=  "+time1+" AND time < " +time2
    print(query)
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Prepare data for the selected attributes
    chart_data = []
    for row in rows:
        data_point = {}
        data_point['time'] = row[0]
        for i, attribute in enumerate(['latitude', 'mag', 'place']):
            if attribute in selected_attributes:
                data_point[attribute] = str(row[i+1])
        print("DATA: ",data_point)
        chart_data.append(data_point)
    print("CHART DATA",chart_data)
    # Render the template with the chart data and selected attributes
        # Render the template with the chart data and selected attributes
    if (selected_plot[0] == 'ScatterPlot'):
        return render_template('scatterplot.html', chart_data=json.dumps(chart_data), selected_attributes=selected_attributes)
    if (selected_plot[0] == 'BarChart'):
        return render_template('histplot.html', chart_data=json.dumps(chart_data), selected_attributes=selected_attributes)
    if (selected_plot[0] == 'PieChart'):
        return render_template('piechart.html', chart_data=json.dumps(chart_data), selected_attributes=selected_attributes)
    return render_template('retry.html')



# port = os.getenv('PORT', '8787')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8587, debug=True)