from google.cloud import aiplatform
from lib.config import Configurations
from lib.deploy import deploy_model

deployment_configs = Configurations()
 
SERVE_DOCKER_URI =deployment_configs.SERVICE_ACCOUNT
PROJECT_ID = deployment_configs.SERVICE_ACCOUNT
REGION = deployment_configs.SERVICE_ACCOUNT
MODEL_NAME = deployment_configs.SERVICE_ACCOUNT
SERVICE_ACCOUNT = deployment_configs.SERVICE_ACCOUNT



print("Model deployment script loaded.") 
model, endpoint = deploy_model(
    model_id="stabilityai/stable-diffusion-2-1",
    task="text-to-image"
)

print("Model deployed successfully.") 
instances = [{"text": "a fox"}]
parameters = {
    "height": 768,
    "width": 768,
    "num_inference_steps": 25,
    "guidance_scale": 7.5,
}

# Perform a prediction
response = endpoint.predict(instances=instances, parameters=parameters)

# Display prediction results
print(f"Prediction results: {response.predictions}")
