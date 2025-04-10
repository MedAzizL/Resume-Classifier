import onnxruntime as ort
from transformers import AutoTokenizer
from typing import Dict
import numpy as np

class ResumeClassifier:
    
    def __init__(self):
        self.categories = [
            "Software Engineer", "Data Scientist", "Product Manager", "UI/UX Designer",
            "Marketing Manager", "Sales Representative", "Business Analyst", "Project Manager",
            "Data Analyst", "DevOps Engineer", "Full Stack Developer", "Machine Learning Engineer",
            "Cybersecurity Analyst", "Cloud Architect", "Mobile Developer", "QA Engineer",
            "Technical Writer", "System Administrator", "Network Engineer", "Database Administrator",
            "Finance & Accounting", "Human Resources"
        ]
        
        try:
            print("Loading fine-tuned model...")
            self.tokenizer = AutoTokenizer.from_pretrained('./models/resume-classifier')
            self.session = ort.InferenceSession('./models/resume-classifier/model.onnx')
            
            import joblib
            label_encoder = joblib.load('./models/resume-classifier/label_encoder.pkl')
            self.categories = list(label_encoder.classes_)
            
            self.use_zero_shot = False
            print(f"Fine-tuned model loaded! Categories: {len(self.categories)}")
            
        except Exception as e:
            print(f"Could not load fine-tuned model ({str(e)}), using zero-shot classification")
            from transformers import pipeline
            self.zero_shot_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
            self.use_zero_shot = True
    
    def classify(self, text: str, top_k: int = 3) -> Dict:
        if self.use_zero_shot:
            return self._classify_zero_shot(text, top_k)
        else:
            return self._classify_fine_tuned(text, top_k)
    
    def _classify_fine_tuned(self, text: str, top_k: int = 3) -> Dict:
        inputs = self.tokenizer(text, truncation=True, max_length=512, padding='max_length', return_tensors='np')
        
        ort_inputs = {
            'input_ids': inputs['input_ids'].astype(np.int64),
            'attention_mask': inputs['attention_mask'].astype(np.int64)
        }
        
        outputs = self.session.run(None, ort_inputs)
        logits = outputs[0][0]
        
        exp_logits = np.exp(logits - np.max(logits))
        probabilities = exp_logits / exp_logits.sum()
        
        top_indices = np.argsort(probabilities)[::-1][:top_k]
        
        predictions = []
        for idx in top_indices:
            predictions.append({
                'category': self.categories[idx],
                'confidence': float(probabilities[idx])
            })
        
        return {
            'category': predictions[0]['category'],
            'confidence': predictions[0]['confidence'],
            'top_predictions': predictions,
            'model_type': 'fine-tuned'
        }
    
    def _classify_zero_shot(self, text: str, top_k: int = 3) -> Dict:
        max_length = 1024
        if len(text) > max_length:
            text = text[:max_length]
        
        result = self.zero_shot_classifier(text, candidate_labels=self.categories, multi_label=False)
        
        predictions = []
        for label, score in zip(result['labels'][:top_k], result['scores'][:top_k]):
            predictions.append({
                'category': label,
                'confidence': float(score)
            })
        
        return {
            'category': predictions[0]['category'],
            'confidence': predictions[0]['confidence'],
            'top_predictions': predictions,
            'model_type': 'zero-shot'
        }
