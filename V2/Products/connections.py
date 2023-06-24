## script to connect ot the SQL Server database
import pyodbc
import sqlalchemy
import shopify


## Function to open the connection to my SQL Server database
def opendbConnMSSQL(server:str,db:str,user:str,password:str,port:str = '3306',driver:str = 'ODBC Driver 17 for SQL Server'):
    """Function to connect to a Sql Server Database.

    Args:
        server (str): This is the server of the SQL Server DB.
        db (str): This is the name of the SQL Server DB.
        user (str): This is the username of the account of the SQL DB.
        password (str): This is the password of the account of the SQL DB.
        port (str): This is the port for use to connect to the SQL DB.
        driver (str): This is the driver for use to connect to the SQL DB.
    Returns:
        conn: returns the sqlalchemy connection 

    """ 
    ##Prepare the engine
    engine = sqlalchemy.create_engine(rf"mssql+pyodbc://{user}:{password}@{server}/{db}?driver={driver.replace(' ','+')}")


    ##Return the connection
    return engine


def shopifyConnect(api_key:str,api_secret:str,shop_url:str,api_version:str,acces_token:str):
    """Function to connect to a Shopify Store through the API.

    Args:
        api_key (str): This is the Api Key of the Shopify Store.
        api_secret (str): This is the Api Secret of the Shopify Store.
        shop_url (str): This is the Shop URL of the Shopify Store.
        api_version (str): This is the API Version in format ('YYYY-MM') check API docs for the versions.
        access_token (str): This is the store API access token.
    Returns:
        session: returns the shopify session 

    """
    shopify.Session.setup(api_key=api_key,secret=api_secret)

    session = shopify.Session(shop_url,api_version,acces_token)

    return session
