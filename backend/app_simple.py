from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from werkzeug.utils import secure_filename
import os
import traceback

app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'doc', 'txt'}

Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

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
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Mock classification for now
        mock_classification = {
            'category': 'Software Engineer',
            'confidence': 0.85,
            'top_predictions': [
                {'category': 'Software Engineer', 'confidence': 0.85},
                {'category': 'Data Scientist', 'confidence': 0.10},
                {'category': 'Product Manager', 'confidence': 0.05}
            ],
            'model_type': 'mock'
        }
        
        mock_parsed_data = {
            'email': 'user@example.com',
            'phone': '+1234567890',
            'skills': ['Python', 'JavaScript', 'React'],
            'education': 'Bachelor of Computer Science',
            'experience_years': 3
        }
        
        return jsonify({
            'classification': mock_classification,
            'parsed_data': mock_parsed_data
        })
        
    except Exception as e:
        print(f"Error processing resume: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Error processing resume: {str(e)}'}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify({
        'categories': [
            "Software Engineer", "Data Scientist", "Product Manager", "UI/UX Designer",
            "Marketing Manager", "Sales Representative", "Business Analyst", "Project Manager",
            "Data Analyst", "DevOps Engineer", "Full Stack Developer", "Machine Learning Engineer",
            "Cybersecurity Analyst", "Cloud Architect", "Mobile Developer", "QA Engineer",
            "Technical Writer", "System Administrator", "Network Engineer", "Database Administrator",
            "Finance & Accounting", "Human Resources"
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
