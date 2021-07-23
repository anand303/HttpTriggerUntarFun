import logging
import json
import tarfile
import random
import azure.functions as func
import os
import shutil
from azure.storage.blob import BlobClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        sourcePath = 'tar/tiff-4.2.0.tar.gz'
        lockboxTarFile = tarfile.open('tar/tiff-4.2.0.tar.gz')
        #index = {i.name: i for i in lockboxTarFile.getmembers()}
        #fileName = random.choice(index.keys())  
        name = "{ \"Files\"" +":["
        #if tarfile.is_tarfile(lockboxTarFile):
        for fileName in lockboxTarFile.getnames():
            #name +=  "\"" + fileInfo.name + "\"" + ","
            if os.path.exists(fileName):
                shutil.rmtree(fileName)
        #name = name.rstrip(name[-1])
        #name = name + "] }"
        #name = SaveUnTarFile(sourcePath)
        #lockboxTarFile.extractall('untar')
        #lockboxTarFile.close()
        
        return func.HttpResponse(f"{name}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
       
def SaveUnTarFile(sourcePath):
    #From Config
    connectionString = "DefaultEndpointsProtocol=https;AccountName=untarblobfunction;AccountKey=ipgr6LlqX1CPNefbUC8foMqRFeYcoqbtdLjEEKAqC2RILhCvbvmT/8qCcs9u/VVyo0pjqGTzKV3XSygfd8lbQQ==;EndpointSuffix=core.windows.net"
    #From Config
    containerName = "temp"
    lockboxTarFile = tarfile.open('tar/tiff-4.2.0.tar.gz')
    for fileName in lockboxTarFile.getnames():        
        lockboxTarFile.extract(fileName)          
        blob = BlobClient.from_connection_string(connectionString,
                                                container_name=containerName,
                                                blob_name=fileName)
                   
        blob.upload_blob(fileName, overwrite=True)
        #print(fileName)
        #with open(fileName, "rb") as f:
            #blob.upload_blob(f, overwrite=True)
        #os.remove(fileName)
    return "Uploaded Successfully..."