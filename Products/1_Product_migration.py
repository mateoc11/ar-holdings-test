## Script to migrate the products from csv files to a SQL Server Database
import pandas as pd
from db_conn import open_dbConnMSSQL
import Keys

##Creation of the products table

def migrateProducts(route:str,server:str,db:str,user:str,pwd:str,pk_column:str = 'ID',create_pk:bool = False):
    
    try:
        ##Read the csv file
        df = pd.read_csv(route)

        ##Open the connection to the database
        conn = open_dbConnMSSQL(server,db,user,pwd)

        ##Migrate the data to the sql database
        df.to_sql("Products",conn,index=False,index_label=f"{pk_column}",if_exists='append')
        
        ## if the pk is not already defined create it if create_pk is True
        if create_pk:
            ##Make the pk column not null to avoid errors
            conn.execute(f"ALTER TABLE Products ALTER COLUMN {pk_column} bigint NOT NULL;")

            ##Make the columnd the primary key
            conn.execute(f"ALTER TABLE Products ADD PRIMARY KEY ({pk_column});")

        ##Close the connection
        conn.close()

        ##Return the succesfull confirmation
        return "Succesfully uploaded the data to the Products table"
    except Exception as e:
        ##Return the error message
        return (str)(e)



##Execute the migration
print(migrateProducts("./Data/sample_data.csv",
                      "LAPTOP-M8D05K6L\SQLEXPRESS",
                      "ar_holdings",
                      Keys.sql_user,
                      Keys.sql_pwd,
                      create_pk=True))