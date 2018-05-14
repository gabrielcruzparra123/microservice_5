#!/usr/bin/python
#pip install mysqlclient
#pythonmicroservice.c7v0hpe7htge.us-east-2.rds.amazonaws.com
import pika
import MySQLdb
import json
import requests
import sys
import decimal
from flask import Flask, request 

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)



class Microservice:

    app = Flask(__name__)

    @app.route('/microservicepython_5/busqueda_stock_producto', methods=['GET','POST'])
    def microserviceLogic ():

        try:
            if request.method =="GET":    
                
                criteria = request.args.get('id_producto')    

                db = MySQLdb.connect(host="microservices.c2v15my6uhyr.us-east-2.rds.amazonaws.com", user="root", passwd="uniandes1",  port=3306, db="microservices", charset='utf8',use_unicode=True)        
                cur = db.cursor()
                query = ("SELECT * FROM stock WHERE id = %s")
                cur.execute(query, [criteria])
                rows = cur.fetchall()
                items =[]
                

                columns = [desc[0] for desc in cur.description]
                result = []
                for row in rows:
                    row = dict(zip(columns, row))
                    result.append(row)    

                items = json.dumps({'stock':result}, indent=4, sort_keys=True, cls=DecimalEncoder)    

                db.close()
                
                return items


            if request.method =="POST":    
                if request.get_json()!= None:
                    req_data =request.get_json()
                    criteria = req_data['id_producto']
                else:
                    criteria = request.args.get('id_producto')
                    
                db = MySQLdb.connect(host="microservices.c2v15my6uhyr.us-east-2.rds.amazonaws.com", user="root", passwd="uniandes1",  port=3306, db="microservices", charset='utf8',use_unicode=True)        
                cur = db.cursor()
                query = ("SELECT * FROM stock WHERE id = %s")
                cur.execute(query, [criteria])
                rows = cur.fetchall()
                items =[]
                
                columns = [desc[0] for desc in cur.description]
                result = []
                for row in rows:
                    row = dict(zip(columns, row))
                    result.append(row)    

                items = json.dumps({'stock':result}, indent=4, sort_keys=True, cls=DecimalEncoder)   
                
                db.close()
                
                return items               
        except IOError as e:
            print ("Error en conexion a url ".url)

    if __name__ == '__main__':
        app.run(host="0.0.0.0", debug=True, port=5004)
        

#Microservice.microserviceLogic(sys.argv[1], sys.argv[2], sys.argv[3])
#Microservice.get_http(sys.argv[3])
#Microservice.queuePublishMessage()

   

