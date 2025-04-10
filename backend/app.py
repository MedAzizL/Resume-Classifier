from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from werkzeug.utils import secure_filename
import os
import traceback

from services.classifier import ResumeClassifier
from services.resume_parser import ResumeParser
from utils.file_handler import FileHandler

app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'doc', 'txt'}

Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

resume_parser = ResumeParser()
classifier = ResumeClassifier()
file_handler = FileHandler(app.config['ALLOWED_EXTENSIONS'])

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'Resume Classifier API',
        'version': '1.0.0'
    })

@app.route('/api/classify', methods=['POST'])
def classify_resume():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file_handler.allowed_file(file.filename):
            return jsonify({
                'error': f'Invalid file type. Allowed types: {", ".join(app.config["ALLOWED_EXTENSIONS"])}'
            }), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            text = resume_parser.extract_text(filepath)
            
            if not text or len(text.strip()) < 50:
                return jsonify({'error': 'Could not extract meaningful text from the file'}), 400
            
            parsed_data = resume_parser.parse_resume(text)
            classification = classifier.classify(text)
            
            result = {
                'classification': classification,
                'parsed_data': parsed_data,
                'text_preview': text[:500] + ('...' if len(text) > 500 else '')
            }
            
            return jsonify(result), 200
            
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        print(f"Error processing resume: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Error processing resume: {str(e)}'}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify({
        'categories': classifier.categories
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
