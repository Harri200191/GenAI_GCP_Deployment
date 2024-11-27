from lib.config import Configurations
from lib.deploy import Deploy

deployment_configs = Configurations()
deploy_object = Deploy() 

print("Model deployment script loaded.") 

model, endpoint = deploy_object.deploy_model(
    model_id="stabilityai/stable-diffusion-2-1",
    task="text-to-image"
)

instances, parameters = deployment_configs.extract_elements("assets/config.json")
response = deploy_object.inference_test(endpoint, instances, parameters)
print(response)