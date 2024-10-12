import fitz  # PyMuPDF
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
from PIL import Image
import io
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

    # Read the file into memory
    pdf_bytes = file.read()

    # Convert PDF to images using PyMuPDF
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    image_files = []

    with tempfile.TemporaryDirectory() as temp_dir:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_path = os.path.join(temp_dir, f"page_{page_num + 1}.png")
            img.save(img_path, format="PNG")
            image_files.append(img_path)

        doc.close()

        # Send the first image file
        if image_files:
            return send_file(image_files[0], mimetype='image/png')
        else:
            return jsonify({'error': 'No images generated'}), 500

application = app

if __name__ == '__main__':
    app.run(debug=True)