from flask import Flask, jsonify
import os
import logging

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

@app.route('/')
def index():
    logging.info("Root endpoint accessed")
    return jsonify({"message": "Hello from Flask on ECS Fargate"})

@app.route('/healthz')
def health():
    logging.info("Health check endpoint hit")
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logging.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port)