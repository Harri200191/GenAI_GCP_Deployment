from flask import Flask, request, jsonify
from google.cloud import aiplatform
import logging

app = Flask(__name__)

# Initialize Vertex AI endpoint
ENDPOINT_NAME = "projects/140506736101/locations/us-central1/endpoints/8430889135530573824/operations/9219847449252724736"
aiplatform.init(project="140506736101", location="us-central1")
endpoint = aiplatform.Endpoint(endpoint_name=ENDPOINT_NAME)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        instances = data.get("instances", [])
        parameters = data.get("parameters", {})
        
        if not instances:
            return jsonify({"error": "No instances provided"}), 400
        
        logging.info("Received prediction request with parameters: %s", parameters)
        
        # Make prediction
        response = endpoint.predict(instances=instances, parameters=parameters)
        return jsonify(response.predictions)
    
    except Exception as e:
        logging.error("Error during prediction: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
