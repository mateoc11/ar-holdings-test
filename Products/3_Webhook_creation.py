import shopify
import Keys

try:
    ##setup the connections to shopify
    shopify.Session.setup(api_key=Keys.api_key, secret=Keys.secret)

    session = shopify.Session(Keys.shop_url,'2023-04',Keys.access_token)

    ##activate the session
    shopify.ShopifyResource.activate_session(session)


    shopify.Webhook.create({"topic":"products/update",
                        "address": "https://azla-webhook-mcgstore.azurewebsites.net:443/api/logs-products-updates/triggers/When_a_HTTP_request_is_received/invoke?api-version=2022-05-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=iqIfnLLVzC0BESfqYEWP0Vd57BtyxE1YWxziec5Qrgg",
                        "format":"json"})

    shopify.ShopifyResource.clear_session()

except Exception as e:
    
    print(str)(e)