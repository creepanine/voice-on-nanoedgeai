import torch
from model import MobileNetV2

# 加载已量化的模型参数
model = MobileNetV2()
model.load_state_dict(torch.load('mobilenetv2_face_quantized.pth'))
model.eval()

# 设置 dummy 输入（1 个样本，1 通道，64x64）
dummy_input = torch.randn(1, 1, 64, 64)

# ONNX 导出路径
onnx_output_path = 'mobilenetv2_face_quantized.onnx'

# 导出 ONNX 模型
torch.onnx.export(
    model, 
    dummy_input,
    onnx_output_path,
    export_params=True,
    opset_version=13,
    do_constant_folding=True,
    input_names=['input'],
    output_names=['output'],