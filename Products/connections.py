## script to connect ot the SQL Server database
import pyodbc
import sqlalchemy
import shopify


## Function to open the connection to my SQL Server database
def open_dbConnMSSQL(server:str,db:str,user:str,password:str,port:str = '3306',driver:str = 'ODBC Driver 17 for SQL Server'):

    ##Prepare the engine
    engine = sqlalchemy.create_engine(rf"mssql+pyodbc://{user}:{password}@{server}/{db}?driver={driver.replace(' ','+')}")
    
    ##Connect to the db
    conn = engine.connect()

    ##Return the connection
    return conn


def shopify_connect(api_key:str,api_secret:str,shop_url:str,api_version:str,acces_token:str):

    shopify.Session.setup(api_key=api_key,secret=api_secret)

    session = shopify.Session(shop_url,api_version,acces_token)

    return session
