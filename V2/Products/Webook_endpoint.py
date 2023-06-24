from flask import Flask,request
from connections import opendbConnMSSQL
import Keys
import json

app = Flask(__name__)

@app.route('/shopify_webhook_endpoint',methods=['POST'])
def endpoint():
	##setup the connection to the SQL Server DB
	if request.method == 'POST':
		engine = opendbConnMSSQL("LAPTOP-M8D05K6L\SQLEXPRESS","ar_holdings",Keys.sql_user,Keys.sql_pwd)
		data = request.get_json()
		conn = engine.connect()
		conn.execute(f"""INSERT INTO Products_updates_log(Updated_at,Product_name,Product_description,Product_id) 
	                    VALUES('{data['updated_at'][:-6]}','{data['title']}','{data['body_html']}','{data['id']}')""")
		conn.close()
		return 'successfully added row to the logs table', 200
	else:
		return '',200

if __name__ == '__main__':
	app.run(port=8080)
	

