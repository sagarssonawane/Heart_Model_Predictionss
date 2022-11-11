from flask import Flask,render_template,request,jsonify
import pickle
import config
import json
import numpy as np
from flask_mysqldb import MySQL
app = Flask(__name__)
# Will take user input >> HTML1 
# pip install flask_mysqldb
# PREDICTION AND USER >> DATABASE SQL
# HTML2 >> OUTPUT 
############################## MYSQL CONFIGURATION STEP####################
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Sagars@1992"
app.config["MYSQL_DB"] = "HEART_DATABASE"
mysql = MySQL(app)

with open(config.MODEL_FILE_PATH,"rb") as f:
     model = pickle.load(f)
with open(config.HYPERPara_FILE_PATH,"rb") as file:
    HYPERPara_ = pickle.load(file)
with open(config.JSON_FILE_PATH,"r") as file:
    json_data = json.load(file)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict1",methods = ["GET","POST"])
def predict():
    data = request.form
    test_array = np.zeros(13)
    test_array[0] = int(data['age'])
    a = test_array[0]
    test_array[1] = int(data['sex'])
    b = test_array[1]
    test_array[2] = int(data['CP'])
    c = test_array[2]
    test_array[3] = int(data['trestbps'])
    d = test_array[3]
    test_array[4] = int(data['chol'])
    e = test_array[4]
    test_array[5] = int(data['fbs'])
    f = test_array[5]
    test_array[6] = int(data['restecg'])
    g = test_array[6]
    test_array[7] = int(data['thalach'])
    h = test_array[7]
    test_array[8] = int(data['exang'])
    i = test_array[8]
    test_array[9] = int(data['oldpeak'])
    j = test_array[9]
    test_array[10] = int(data['slope'])
    k = test_array[10]
    test_array[11] = int(data['ca'])
    l = test_array[11]
    test_array[12] = int(data['thal'])
    m = test_array[12]
    std_array = HYPERPara_.transform([test_array])
    # print(std_scalar)
    z = model.predict(std_array)
    z1 = np.round(z[0],2)
    cursor = mysql.connection.cursor()
    query = 'CREATE TABLE IF NOT EXISTS HEART_PURITY(age VARCHAR(20),sex VARCHAR(20),CP VARCHAR(20),trestbps VARCHAR(20),chol VARCHAR(20),fbs VARCHAR(20),restecg VARCHAR(20),thalach VARCHAR(20),exang VARCHAR(20),oldpeak VARCHAR(20),slope VARCHAR(20),ca VARCHAR(20),thal VARCHAR(20),target VARCHAR(20))'
    cursor.execute(query)
    cursor.execute('INSERT INTO HEART_PURITY(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(a,b,c,d,e,f,g,h,i,j,k,l,m,z1))

    mysql.connection.commit()
    cursor.close()

    return render_template("index2.html",z1=z1)

if __name__ =="__main__":
    app.run(host="0.0.0.0",port=config.PORT_NUMBER)




 