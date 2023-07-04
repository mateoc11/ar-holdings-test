import json
import requests

def createWebhook(shop_url:str,access_token:str,topic:str,address:str,r_format:str):
    """Function to create a Webhook of a Shopify Store.

    Args:
        access_token (str): this is the access token of the store using the API. 
        shop_url (str): this is the shop url of the store. 
        topic (str): this the event that triggers the webhook. (check docs for allowed topics)
        address (str): this is the endpoint address to which the webhook should send the POST request
        r_format (str): this is the format in which the webhook subscription should send the data.
    Returns:
        None

    """ 
    
    try:
        ##Required headers for post request
        headers = {"Content-Type":"application/json","X-Shopify-Access-Token": f'{access_token}'}

        ##built the webhook JSON
        webhook_json ={"webhook":{}}
        webhook_json["webhook"]['address'] = address
        webhook_json["webhook"]['topic'] = topic
        webhook_json["webhook"]['format'] = r_format

        ##send the request
        r = requests.post(f'{shop_url}/admin/api/2023-04/webhooks.json', data=json.dumps(webhook_json), headers=headers)

        ##Print Webhook
        print(r.json())
        
        return r


    except Exception as e:
        
        print(e)
