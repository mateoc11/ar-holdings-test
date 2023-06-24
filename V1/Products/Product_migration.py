## Script to migrate the products from csv files to a SQL Server Database
import pandas as pd
import numpy as np
import sqlalchemy
##Creation of the products table

def migrateProducts(route:str,sql_conn,pk_column:str = 'ID',create_pk:bool = False):
    """Function to migrate the products from a csv file to a sql server db.

    Args:
        route (str): this is the route of the csv file.
        sql_conn : this is the sqlalchemy connection to the SQL Server DB.
        pk_column(str): This is the name of the primary key column.
        create_pk(bool): Specifies if the code should add the PK constraint to the previous parameter  
    Returns:
        str: success message

    """ 
   
    try:
        ##Read the csv file
        df = pd.read_csv(route)

        ##add the sync column to the df
        df['synchronized_at']= np.nan

        ##Migrate the data to the sql database
        df.to_sql("Products",sql_conn,index=False,index_label=f"{pk_column}",if_exists='append',dtype={'synchronized_at': sqlalchemy.DateTime()})

        ## if the pk is not already defined create it if create_pk is True
        if create_pk:
            ##Make the pk column not null to avoid errors
            sql_conn.execute(f"ALTER TABLE Products ALTER COLUMN {pk_column} bigint NOT NULL;")

            ##Make the columnd the primary key
            sql_conn.execute(f"ALTER TABLE Products ADD PRIMARY KEY ({pk_column});")


        print("Succesfully uploaded the data to the Products table")
        ##Return the succesfull confirmation
        return "Succesfully uploaded the data to the Products table"
    except Exception as e:
        print(e)

