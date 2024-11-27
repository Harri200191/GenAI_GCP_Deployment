from google.cloud import aiplatform

# Set constants for deployment
SERVE_DOCKER_URI = "us-docker.pkg.dev/deeplearning-platform-release/vertex-model-garden/pytorch-inference.cu125.0-1.ubuntu2204.py310"
PROJECT_ID = "cc-assignment-2-442707"
REGION = "us-central1"
MODEL_NAME = "stable-diffusion-2-1"
SERVICE_ACCOUNT = "140506736101-compute@developer.gserviceaccount.com"

def deploy_model(model_id, task):
    """Create a Vertex AI Endpoint and deploy the specified model to the endpoint."""

    # Initialize AI Platform
    aiplatform.init(project=PROJECT_ID, location=REGION)

    # Create endpoint
    endpoint = aiplatform.Endpoint.create(display_name=f"{MODEL_NAME}-{task}-endpoint")
    print(f"Endpoint created: {endpoint.resource_name}")

    # Define serving environment
    serving_env = {
        "MODEL_ID": model_id,
        "TASK": task,
        "DEPLOY_SOURCE": "custom",
    }

    # Upload model
    model = aiplatform.Model.upload(
        display_name=MODEL_NAME,
        serving_container_image_uri=SERVE_DOCKER_URI,
        serving_container_ports=[7080],
        serving_container_predict_route="/predict",
        serving_container_health_route="/health",
        serving_container_environment_variables=serving_env,
    )
    print(f"Model uploaded: {model.resource_name}")

    # Define machine configuration
    machine_type = "g2-standard-8"  # Adjust as needed
    accelerator_type = "NVIDIA_L4"
    accelerator_count = 1

    # Deploy model to the endpoint
    model.deploy(
        endpoint=endpoint,
        machine_type=machine_type,
        accelerator_type=accelerator_type,
        accelerator_count=accelerator_count,
        deploy_request_timeout=1800,
        service_account=SERVICE_ACCOUNT,
    )
    print(f"Model deployed to endpoint: {endpoint.resource_name}")

    return model, endpoint

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
