from google.cloud import aiplatform
from lib.config import Configurations

class Deploy:
    def __init__(self):
        deployment_configs = Configurations()

    def deploy_model(self, model_id, task):
        """
            Create a Vertex AI Endpoint and deploy the specified model to the endpoint.

            Args:
                model_id: str, the model ID to deploy.
                task: str, the task type of the model.

            Returns:
                model: Vertex AI Model resource.
                endpoint: Vertex AI Endpoint resource.
        """

        # Initialize AI Platform
        aiplatform.init(project=self.deployment_configs.PROJECT_ID, location=self.deployment_configs.REGION)

        # Create endpoint
        endpoint = aiplatform.Endpoint.create(display_name=f"{self.deployment_configs.MODEL_NAME}-{task}-endpoint")
        print(f"Endpoint created: {endpoint.resource_name}")

        # Define serving environment
        serving_env = {
            "MODEL_ID": model_id,
            "TASK": task,
            "DEPLOY_SOURCE": "custom",
        }

        # Upload model
        model = aiplatform.Model.upload(
            display_name=self.deployment_configs.MODEL_NAME,
            serving_container_image_uri=self.deployment_configs.SERVE_DOCKER_URI,
            serving_container_ports=[7080],
            serving_container_predict_route="/predict",
            serving_container_health_route="/health",
            serving_container_environment_variables=serving_env,
        )

        print(f"Model uploaded: {model.resource_name}")

        # Deploy model to the endpoint
        model.deploy(
            endpoint=endpoint,
            machine_type=self.deployment_configs.MACHINE_TYPE,
            accelerator_type=self.deployment_configs.ACCELERATOR_TYPE,
            accelerator_count=self.deployment_configs.ACCELERATOR_COUNT,
            deploy_request_timeout=1800,
            service_account=self.deployment_configs.SERVICE_ACCOUNT,
        )
        print(f"Model deployed to endpoint: {endpoint.resource_name}")

        return model, endpoint
    
    def inference_test(self, endpoint, instances, parameters):
        response = endpoint.predict(instances=instances, parameters=parameters)
        return response
