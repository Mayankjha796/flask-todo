from flask import Flask, jsonify
import os
import logging
import boto3
from botocore.exceptions import ClientError
import json

app = Flask(__name__)

# Local test-friendly logs directory
log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)

# Configure logging
log_file = os.path.join(log_dir, "app.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def get_secret():
    secret_name = "port"  # Name of your AWS Secret
    region_name = os.environ.get("AWS_REGION", "ap-south-1")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        logging.error(f"Error fetching secret '{secret_name}': {e}")
        return None

    secret_str = get_secret_value_response['SecretString']
    try:
        # Parse JSON if stored as {"PORT": "8080"}
        secret_dict = json.loads(secret_str)
        return secret_dict.get("PORT")
    except json.JSONDecodeError:
        # If secret is just a plain string like "8080"
        return secret_str

@app.route('/')
def index():
    logging.info("Root endpoint accessed")
    return jsonify({"message": "Hello from Flask on ECS Fargate"})

@app.route('/healthz')
def health():
    logging.info("Health check endpoint hit")
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    # Fetch port from Secrets Manager or fallback to env/default
    secret_port = get_secret()
    port = int(secret_port or os.environ.get("PORT", 8080))
    logging.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port)
