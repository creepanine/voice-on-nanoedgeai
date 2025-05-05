import torch
import torch.ao.quantization as quant
from model import MobileNetV2

# 1. 初始化模型结构
model = MobileNetV2()
model.eval()

# 2. 加入量化配置
model.qconfig = quant.get_default_qconfig('fbgemm')

# 3. 准备和转换模型结构（必须）
quant.prepare(model, inplace=True)
quant.convert(model, inplace=True)

# 4. 加载量化后的 state_dict（必须是字典）
state_dict = torch.load('mobilenetv2_face_quantized.pth', map_location='cpu')
model.load_state_dict(state_dict)

# 5. 导出为 ONNX
dummy_input = torch.randn(1, 1, 64, 64)  # 单通道
torch.onnx.export(
    model,
    dummy_input,
    "mobilenetv2_face_quantized.onnx",
    input_names=["input"],
    output_names=["output"],
    opset_version=13,
    do_constant_folding=True
)

print("ONNX 导出完成：mobilenetv2_face_quantized.onnx")
