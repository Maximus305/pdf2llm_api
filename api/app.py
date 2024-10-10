import fitz  # PyMuPDF
from flask import Flask, request, jsonify
import os
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Read the file into memory
    pdf_bytes = file.read()

    # Convert PDF to images using PyMuPDF
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    image_data = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = pix.tobytes("png")
        img_base64 = base64.b64encode(img).decode('utf-8')
        image_data.append({
            'page': page_num + 1,
            'image': img_base64
        })

    doc.close()

    return jsonify({'message': 'File converted successfully', 'images': image_data}), 200

if __name__ == '__main__':
    app.run(debug=True)