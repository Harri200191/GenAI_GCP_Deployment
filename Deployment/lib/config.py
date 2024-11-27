import os
from dotenv import load_dotenv

load_dotenv("enviornm.env")

def get(item):
    if os.environ.get(item) != None:
        return os.environ.get(item)
    else:
        return 0
    
class Configurations:
    SERVE_DOCKER_URI = os.getenv("SERVE_DOCKER_URI") 
    PROJECT_ID = os.getenv("PROJECT_ID")  
    REGION =  os.getenv("REGION") or "us-central1"
    MODEL_NAME =  os.getenv("MODEL_NAME") 
    SERVICE_ACCOUNT =  os.getenv("SERVICE_ACCOUNT") 
    MACHINE_TYPE = os.getenv("MACHINE_TYPE")  
    ACCELERATOR_TYPE =  os.getenv("ACCELERATOR_TYPE") 
    ACCELERATOR_COUNT = os.getenv("ACCELERATOR_COUNT")  