# Model Files Required

This directory should contain the following files for the fine-tuned model:

- `model_quantized.onnx` - Quantized ONNX model file (~64MB)
- `label_encoder.pkl` - Label encoder for categories
- `config.json` - Model configuration
- `tokenizer.json` - Tokenizer files

If these files are not present, the application will automatically fall back to zero-shot classification using BART.

## To add model files:

1. Run `python quantize_model.py` locally to generate the quantized model
2. Copy the generated files to this directory
3. Commit and push to GitHub

The application will work with zero-shot classification even without these files.
