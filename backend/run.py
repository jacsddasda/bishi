import sys
print(f"Python version: {sys.version}")
print("Starting resume analysis service...")

from flask import Flask, request, jsonify
from flask_cors import CORS
print("✓ Flask imported")
print("✓ Flask-CORS imported")

from app.services.pdf_parser import parse_pdf
print("✓ pdf_parser imported")

from app.services.info_extractor import extract_info
print("✓ info_extractor imported")

from app.services.resume_scorer import score_resume
print("✓ resume_scorer imported")

from app.utils.cache import get_cache, set_cache
print("✓ cache imported")

import os
print("✓ os imported")

print("Creating Flask app...")
app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
# Initialize CORS to allow cross-origin requests
CORS(app)
print("✓ Flask app created")
print("✓ CORS initialized")
print(f"✓ Static folder: {app.static_folder}")

# Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    print("✓ Uploads directory created")
else:
    print("✓ Uploads directory already exists")

@app.route('/api/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    # Save the file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Check cache first
    cache_key = f"resume:{file.filename}"
    cached_result = get_cache(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    # Parse PDF
    try:
        text = parse_pdf(filepath)
    except Exception as e:
        return jsonify({'error': f'Failed to parse PDF: {str(e)}'}), 500
    
    # Extract information
    try:
        info = extract_info(text)
    except Exception as e:
        return jsonify({'error': f'Failed to extract information: {str(e)}'}), 500
    
    # Store in cache
    result = {'text': text, 'info': info}
    set_cache(cache_key, result)
    
    return jsonify(result)

@app.route('/api/score', methods=['POST'])
def score_resume_endpoint():
    data = request.get_json()
    if not data or 'resume_info' not in data or 'job_description' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    resume_info = data['resume_info']
    job_description = data['job_description']
    
    # Calculate score
    try:
        score = score_resume(resume_info, job_description)
    except Exception as e:
        return jsonify({'error': f'Failed to score resume: {str(e)}'}), 500
    
    return jsonify({'score': score})

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/frontend/<path:path>')
def send_frontend(path):
    return app.send_static_file(f'frontend/{path}')

if __name__ == '__main__':
    print("Starting server on http://0.0.0.0:5000...")
    app.run(debug=True, host='0.0.0.0', port=5000)
    print("Server stopped")

