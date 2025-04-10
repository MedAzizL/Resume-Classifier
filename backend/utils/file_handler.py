from typing import Set

class FileHandler:
    
    def __init__(self, allowed_extensions: Set[str]):
        self.allowed_extensions = allowed_extensions
    
    def allowed_file(self, filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
