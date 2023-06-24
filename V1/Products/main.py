from connections import opendbConnMSSQL,shopifyConnect
import shopify
from Product_migration import  migrateProducts
from Product_publishing import publishProducts
from Webhook_creation import createWebhook
import Keys

##setup the connection to the SQL Server DB
engine = opendbConnMSSQL("LAPTOP-M8D05K6L\SQLEXPRESS","ar_holdings",Keys.sql_user,Keys.sql_pwd)

##Connect to the db
conn = engine.connect()

##Get the shopify session
shopify_session = shopifyConnect(Keys.api_key,Keys.secret,Keys.shop_url,'2023-04',Keys.access_token)

##Execute the migration
migrateProducts("./Data/sample_data.csv",conn,create_pk=True)

'''##Publish the produts on the shopify store
publishProducts(conn,shopify_session,True)

##Create the webhook
createWebhook(shopify_session,"products/update",Keys.endpoint,"json")'''