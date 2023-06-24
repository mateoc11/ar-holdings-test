import pandas as pd
from datetime import datetime
import json
import requests


def publishProducts(sql_conn,access_token:str,shop_url:str,create_collections:bool = False):
    """Function to publish products from the SQL Server table to a Shopify Store.

    Args:
        sql_conn : this is the sqlalchemy connection to the SQL Server DB.
        access_token (str): this is the access token of the store using the API. 
        shop_url (str): this is the shop url of the store. 
        create_collections (bool): this is specifies if the user wants to create clothe type collections or not.
    Returns:
        None

    """ 

    conn = sql_conn
    headers = {"Content-Type":"application/json","X-Shopify-Access-Token": f'{access_token}'}

    try:
        if create_collections:
            ##make a query to extrach the diffetent types of products
            df = pd.read_sql_query("SELECT DISTINCT(Categories) FROM Products",conn)

        
            ##Split the strings and drop the duplicates to have only the required values
            categories = df['Categories'].apply(lambda x: x.split('|')[0].split('>')[-1]).T.drop_duplicates().values


            ##For every type of product we create a smart collection that will detect the tags of the products
            for clothe_type in categories:
                ##We create the dictionay(JSON) that defines the smartcollection structure
                collection = {"smart_collection":{"title":f'{clothe_type}',"rules":[{"column":"tag","relation":"equals","condition":f'{clothe_type}'}]}}
                
                ##specify url of the smartcollection endpoint
                post_url = f"{shop_url}/admin/api/2023-04/smart_collections.json"

                ##Send the request
                r = requests.post(post_url, data=json.dumps(collection), headers=headers)


        ## Now we extract all the product info on the parent or simple items
        parents = pd.read_sql_query("SELECT * FROM Products WHERE Parent is NULL and synchronized_at is NULL",conn)

        ## For every parent we search his variants, add the required information, and link the images
        for SKU in parents['SKU'].values:
            print(SKU)
            
            ##Query to extract all the variants
            df = pd.read_sql_query(f"SELECT * FROM Products WHERE SKU LIKE '{SKU}%' ORDER BY ID DESC",conn)

            ##Initialize product
            product = {"product":{}}
            
            ##Edge case validation for products that have a different name estructure
            if ';' in df['Name'][0]:
                product['product']['title'] = df['Name'][0].split(';')[1]
            else:
                product['product']['title'] = df['Name'][0].split('-')[0]

            ##Fill the required information
            product['product']['body_html'] =  df['description'][0]
            product['product']['product_type'] = df['Categories'][0].split('|')[0].split('>')[-1]
            product['product']['tags'] = f"{df['Categories'][0].split('|')[0].split('>')[-1]}"
            product['product']['variants'] = []

            ##If type is no simple it means it has multiple variants if not only add one, create the different variants
            if df['Type'][0] != 'simple':
                
                for index, row in df.iterrows():
                    if row['SKU'] == SKU:
                        continue

                    variant = {}
                    variant['option1'] = row['Attribute 1 value(s)']
                    variant['option2'] = row['Attribute 2 value(s)']
                    variant['price'] = row['Regular price']
                    variant['weight'] = row['Weight (lbs)']
                    variant['weight_unit'] = 'lb'
                    variant['sku'] = row["SKU"]
                    variant['inventory_management'] = 'shopify'
                    product['product']['variants'].append(variant)

                
                ## Create the options for the products that have it            
                product['product']['options'] = [{"name": df['Attribute 1 name'][1],"values":(list)(df['Attribute 1 value(s)'].dropna().drop_duplicates().values)},
                        {"name": df['Attribute 2 name'][1],"values":(list)(df['Attribute 2 value(s)'].dropna().drop_duplicates().values)}]
                
            else:
                variant = {}
                variant['title'] = df['Name'][0]
                variant['price']= df['Regular price'][0]
                variant['weight'] = df['Weight (lbs)'][0]
                variant['weight_unit'] = 'lb'
                variant['sku'] = df['SKU'][0]
                variant['inventory_management']  = 'shopify'
                product['product']['variants'].append(variant)
            
            ## save the completed product
            post_url = f"{shop_url}/admin/api/2023-04/products.json"

            ##Get the created product
            r = requests.post(post_url, data=json.dumps(product), headers=headers)

            ##After saving update the sync column to current time for the product and his variants
            conn.execute(f'''UPDATE Products set synchronized_at = '{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' WHERE SKU like '{SKU}%' ''')

            ##Get the location of the store to be able to update the inventory later
            location = requests.get(f"{shop_url}/admin/api/2023-04/locations/85083488533.json", headers={"X-Shopify-Access-Token":access_token}).json()

            ##If the product was created succesfully we update the images and inventory
            if r.status_code == 201:
                r = r.json()
                inventory_url = f"{shop_url}/admin/api/2023-04/inventory_levels/set.json"

                #For every variant of the product update and link the images, and update the stock
                for variant in r['product']['variants']:
                    ##we create the inventory level JSON
                    inventory_json = {"location_id":location['location']['id'],
                                        "inventory_item_id":variant['inventory_item_id'],
                                        "available":(str)(df[df['SKU'] == variant['sku']]['Stock'].values[0])}
                    
                    ##set the stock quantity of the variants
                    requests.post(inventory_url, data=json.dumps(inventory_json), headers=headers)

                    ##We populate the image json
                    image = {"image":{'product_id': r['product']['id'],
                                      'variant_ids': [variant['id']],
                                      'src':df[df['SKU'] == variant['sku']]['Images'].values[0].split(',')[0]
                                      }}

                    
                    ##Assign the image to a product
                    image = requests.post(f"{shop_url}/admin/api/2023-04/products/{r['product']['id']}/images.json", 
                                            data=json.dumps(image), 
                                            headers=headers)
                    
                    ##Assign the image to a product variant
                    variant_json = {"variant":{"id": variant['id'], "image_id": image.json()['image']['id']}}

                    ##Sent the update
                    variant = requests.put(f"{shop_url}/admin/api/2023-04/variants/{variant['id']}.json", 
                                            data=json.dumps(variant_json), 
                                            headers=headers)
                    
    except Exception as e:
        print(e)




    print("Succesfully published the Products to the Shopify store")

