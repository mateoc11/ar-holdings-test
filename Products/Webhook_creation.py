import shopify



def createWebhook(shopify_session,topic:str,address:str,r_format:str):
    """Function to create a Webhook of a Shopify Store.

    Args:
        shopify_session: this is the shopify session of the store using the API. 
        topic (str): this the event that triggers the webhook. (check docs for allowed topics)
        address (str): this is the endpoint address to which the webhook should send the POST request
        r_format (str): this is the format in which the webhook subscription should send the data.
    Returns:
        None

    """ 
    
    try:

        session = shopify_session

        ##activate the session
        shopify.ShopifyResource.activate_session(session)

        ##Create the webhook on products updates and specify endpoint from azure
        shopify.Webhook.create({"topic": topic,
                            "address": address,
                            "format":r_format})


        print("Succesfully created the Webhook of the Shopify store")
        ##Close session
        shopify.ShopifyResource.clear_session()

    except Exception as e:
        
        print(e)
