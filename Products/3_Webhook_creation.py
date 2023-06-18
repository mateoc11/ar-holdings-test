import shopify
import Keys
from connections import shopify_connect


def create_Webhook(shopify_session,topic:str,address:str,r_format:str):
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

        ##Close session
        shopify.ShopifyResource.clear_session()

    except Exception as e:
        
        print(str)(e)

##Get the shopify session
shopify_session = shopify_connect(Keys.api_key,Keys.secret,Keys.shop_url,'2023-04',Keys.access_token)

##create webhhook
create_Webhook(shopify_session,"products/update","https://azla-webhook-mcgstore.azurewebsites.net:443/api/logs-products-updates/triggers/When_a_HTTP_request_is_received/invoke?api-version=2022-05-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=iqIfnLLVzC0BESfqYEWP0Vd57BtyxE1YWxziec5Qrgg","json")