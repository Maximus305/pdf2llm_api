import fitz  # PyMuPDF
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
from io import BytesIO
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": ["https://pdf2llm.vercel.app", "http://localhost:3000", "http://localhost:5173"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

logging.basicConfig(level=logging.DEBUG)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    app.logger.info("Received request to /api/upload")
    app.logger.debug(f"Request headers: {request.headers}")
    app.logger.debug(f"Request files: {request.files}")
    app.logger.debug(f"Request form: {request.form}")

    if 'file' not in request.files:
        app.logger.error("No file part in the request")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        app.logger.error("No selected file")
        return jsonify({'error': 'No selected file'}), 400

    # ... rest of your upload_file function ...

application = app

if __name__ == '__main__':
    app.run(debug=True)