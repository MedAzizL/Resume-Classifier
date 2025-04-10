import re
from typing import Dict, List
from pathlib import Path
import PyPDF2
import docx

class ResumeParser:
    
    def __init__(self):
        self.common_skills = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'express',
            'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
            'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow', 'pytorch',
            'html', 'css', 'sass', 'bootstrap', 'tailwind',
            'rest api', 'graphql', 'microservices', 'agile', 'scrum',
            'linux', 'windows', 'macos', 'bash', 'powershell'
        ]
    
    def extract_text(self, file_path: str) -> str:
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension == '.pdf':
            return self._extract_from_pdf(file_path)
        elif extension in ['.docx', '.doc']:
            return self._extract_from_docx(file_path)
        elif extension == '.txt':
            return self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
    
    def _extract_from_pdf(self, file_path: Path) -> str:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    
    def _extract_from_docx(self, file_path: Path) -> str:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    def _extract_from_txt(self, file_path: Path) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def parse_resume(self, text: str) -> Dict:
        return {
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'urls': self._extract_urls(text),
            'skills': self._extract_skills(text),
            'education': self._extract_education(text),
            'experience_years': self._estimate_experience(text)
        }
    
    def _extract_email(self, text: str) -> str:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else None
    
    def _extract_phone(self, text: str) -> str:
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        matches = re.findall(phone_pattern, text)
        return matches[0].strip() if matches else None
    
    def _extract_urls(self, text: str) -> List[str]:
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        github_pattern = r'github\.com/[\w-]+'
        
        urls.extend(re.findall(linkedin_pattern, text, re.IGNORECASE))
        urls.extend(re.findall(github_pattern, text, re.IGNORECASE))
        
        return list(set(urls))
    
    def _extract_skills(self, text: str) -> List[str]:
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_education(self, text: str) -> List[str]:
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'mba', 'b.s.', 'm.s.',
            'b.a.', 'm.a.', 'b.tech', 'm.tech', 'university', 'college', 'institute'
        ]
        
        education = []
        text_lower = text.lower()
        
        for keyword in education_keywords:
            if keyword in text_lower:
                sentences = re.split(r'[.\n]', text)
                for sentence in sentences:
                    if keyword in sentence.lower() and sentence.strip():
                        education.append(sentence.strip())
                        break
        
        return list(set(education))[:3]
    
    def _estimate_experience(self, text: str) -> int:
        experience_pattern = r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?experience'
        matches = re.findall(experience_pattern, text.lower())
        
        if matches:
            years = [int(match) for match in matches]
            return max(years)
        
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, text)
        
        if len(years) >= 2:
            years = [int(year) for year in years]
            return max(years) - min(years)
        
        return 0
