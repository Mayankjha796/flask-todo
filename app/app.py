from flask import Flask, jsonify
import os

app = Flask(_name_)

@app.route('/')
def index():
    return jsonify({"message": "Hello from Flask on ECS Fargate"})

@app.route('/healthz')
def health():
    return jsonify({"status": "ok"}), 200

if _name_ == '_main_':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)