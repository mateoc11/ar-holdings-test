import shopify
from db_conn import open_dbConnMSSQL
import pandas as pd
import Keys

##open the connection to the SQL Server DB
conn = open_dbConnMSSQL("LAPTOP-M8D05K6L\SQLEXPRESS","ar_holdings","mateoc","test1234")

##setup the connections to shopify
shopify.Session.setup(api_key=Keys.api_key, secret=Keys.secret)

session = shopify.Session(Keys.shop_url,'2023-04',Keys.access_token)

##activate the session
shopify.ShopifyResource.activate_session(session)

##make a query to extrach the diffetent types of products
df = pd.read_sql_query("SELECT DISTINCT(Categories) FROM Products",conn)

##Split the strings and drop the duplicates to have only the required values
categories = df['Categories'].apply(lambda x: x.split('|')[0].split('>')[-1]).T.drop_duplicates().values


##For every type of product we create a smart collection that will detect the tags of the products
for cloth_type in categories:
    shopify.SmartCollection.create({'title': f'{cloth_type}', 'rules': [{'column': 'tag', 'relation': 'equals', 'condition': f'{cloth_type}'}]})


## Now we extract all the product info on the parent or simple items
parents = pd.read_sql_query("SELECT * FROM Products WHERE Parent is NULL",conn)

## For every parent we search his variants, add the required information, and link the images
for SKU in parents['SKU'].values:
    print(SKU)
    
    ##Query to extract all the variants
    df = pd.read_sql_query(f"SELECT * FROM Products WHERE SKU LIKE '{SKU}%' ORDER BY ID DESC",conn)

    ##Initialize product
    product = shopify.Product()
    
    ##Edge case validation for products that have a different name estructure
    if ';' in df['Name'][0]:
        product.title = df['Name'][0].split(';')[1]
    else:
        product.title = df['Name'][0].split('-')[0]

    ##Fill the required information
    product.body_html =  df['description'][0]
    product.product_type = df['Categories'][0].split('|')[0].split('>')[-1]
    product.tags = f"{df['Categories'][0].split('|')[0].split('>')[-1]}"

    ##Initialize required variables
    variants = []
    options = []
    product.variants = []

    ##If type is no simple it means it has multiple variants if not only add one, create the different variants
    if df['Type'][0] != 'simple':
        
        for index, row in df.iterrows():
            if row['SKU'] == SKU:
                continue

            variant = shopify.Variant()
            variant.option1 = row['Attribute 1 value(s)']
            variant.option2 = row['Attribute 2 value(s)']
            variant.price = row['Regular price']
            variant.weight = row['Weight (lbs)']
            variant.weight_unit = 'lb'
            variant.sku = row["SKU"]
            variant.inventory_management = 'shopify'
            product.variants.append(variant)

        ## Create the options for the products that have it            
        options = [{"name": df['Attribute 1 name'][1],"values":(list)(df['Attribute 1 value(s)'].dropna().drop_duplicates().values)},
                   {"name": df['Attribute 2 name'][1],"values":(list)(df['Attribute 2 value(s)'].dropna().drop_duplicates().values)}]
        
        product.options = options
    else:
        variant = shopify.Variant()
        variant.title = df['Name'][0]
        variant.price = df['Regular price'][0]
        variant.weight = df['Weight (lbs)'][0]
        variant.weight_unit = 'lb'
        variant.sku = df['SKU'][0]
        variant.inventory_management = 'shopify'
        product.variants.append(variant)
    
    ## save the completed product
    sucess = product.save() 

    ##Get the location of the store to be able to update the inventory later
    location = shopify.Location.find_first()

    if sucess:
        #For every variant of the product update and link the images, and update the stock
        for variant in product.variants:

            ##set the stock quantity of the variants
            shopify.InventoryLevel.set(location.id,variant.inventory_item_id,(str)(df[df['SKU'] == variant.sku]['Stock'].values[0]))

            image = shopify.Image()
            image.product_id = product.id
            image.variant_ids = [variant.id]
            image.src = df[df['SKU'] == variant.sku]['Images'].values[0].split(',')[0]
            image.save()
            
            variant.image_id = image.id
            variant.save()




shopify.ShopifyResource.clear_session()