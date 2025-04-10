# Model Files

The fine-tuned model files are not included in this repository due to GitHub file size limits.

## Model Structure

The `resume-classifier` folder should contain:
- `model.onnx` (255 MB) - ONNX optimized model for inference
- `model.safetensors` (260 MB) - Original PyTorch model weights
- `tokenizer.json`, `vocab.txt` - Tokenizer files (included)
- `config.json` - Model configuration (included)
- `label_encoder.pkl` - Category mapping (included)

## How to Get the Model

**Option 1: Train Your Own Model**
1. Prepare a dataset of resumes with categories
2. Run the training script (not included - refer to Hugging Face documentation)
3. Convert to ONNX format for production deployment

**Option 2: Use Zero-Shot Classification**
If the fine-tuned model is not available, the system automatically falls back to zero-shot classification using BART, which requires no local model files.

## ONNX Conversion

If you have a PyTorch model, convert it to ONNX:
```python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained('./models/resume-classifier')
tokenizer = AutoTokenizer.from_pretrained('./models/resume-classifier')
dummy_input = tokenizer("Sample text", return_tensors="pt", padding="max_length", max_length=512)

torch.onnx.export(
    model,
    (dummy_input['input_ids'], dummy_input['attention_mask']),
    './models/resume-classifier/model.onnx',
    opset_version=14
)
```

