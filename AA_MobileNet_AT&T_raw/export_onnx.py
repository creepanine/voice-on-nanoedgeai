import torch
from model import MobileNetV2

def export_model_to_onnx(model_path='mobilenetv2_face.pth', onnx_path='mobilenetv2_face.onnx'):
    # 创建模型并加载权重
    model = MobileNetV2()
    model.load_state_dict(torch.load(model_path))
    model.eval()

    # 创建一个示例输入张量（1通道灰度图像，大小64x64）
    dummy_input = torch.randn(1, 1, 64, 64)

    # 导出为 ONNX
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}},
        opset_version=11
    )

    print(f"模型已导出为 {onnx_path}")

if __name__ == '__main__':
    export_model_to_onnx()
