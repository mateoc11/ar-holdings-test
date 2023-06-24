from connections import opendbConnMSSQL
from Product_migration import  migrateProducts
from Product_publishing import publishProducts
from Webhook_creation import createWebhook
import Keys

##setup the connection to the SQL Server DB
engine = opendbConnMSSQL("LAPTOP-M8D05K6L\SQLEXPRESS","ar_holdings",Keys.sql_user,Keys.sql_pwd)

##Connect to the db
conn = engine.connect()

##Execute the migration
migrateProducts("./Data/sample_data.csv",conn,create_pk=True)

##Publish the produts on the shopify store
publishProducts(conn,Keys.access_token,Keys.shop_url,True)

##Create the webhook
createWebhook(Keys.shop_url,Keys.access_token,"products/update",Keys.endpoint,"json")