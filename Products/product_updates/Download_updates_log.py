from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import Token
import os

## Url of the Azure Storage Account
account_url = "https://adlstecnicaltest.blob.core.windows.net" 

try:
    ## Connect to the blob storage using url and SAS TOKEN
    blob_service_client = BlobServiceClient(account_url, credential=Token.sas_token)

    ## Specify the download path 
    download_file_path = os.path.join(".\Products\product_updates", 'updates.log')

    ## Get the right container
    container_client = blob_service_client.get_container_client(container="products-updates") 

    ## Open the locl path in write binary mode (according to official docs)
    ## then write the contents of the right blob using the download_blob method
    with open(file=download_file_path, mode="wb") as download_file:
        download_file.write(container_client.download_blob("updates.log").readall())

except Exception as e:
    
    print(str)(e)
