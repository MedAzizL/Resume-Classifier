import onnx
from onnxruntime.quantization import quantize_dynamic
import os

print("Quantizing model to reduce size...")

input_model = "./models/resume-classifier/model.onnx"
output_model = "./models/resume-classifier/model_quantized.onnx"

# Get original size
original_size = os.path.getsize(input_model) / (1024*1024)
print(f"Original model size: {original_size:.2f} MB")

# Quantize the model
quantize_dynamic(
    input_model,
    output_model,
    weight_type=onnx.TensorProto.INT8
)

# Get new size
new_size = os.path.getsize(output_model) / (1024*1024)
print(f"Quantized model size: {new_size:.2f} MB")
print(f"Size reduction: {((original_size - new_size) / original_size * 100):.1f}%")

print("Quantization complete!")

