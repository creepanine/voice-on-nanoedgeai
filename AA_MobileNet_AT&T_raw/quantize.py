# import torch
# import torch.ao.quantization as quant
# from model import MobileNetV2
# from dataset import RawFaceDataset
# from torchvision import transforms
# from torch.utils.data import DataLoader

# #加载已训练模型
# model = MobileNetV2()
# model.load_state_dict(torch.load('mobilenetv2_face.pth'))
# model.eval()

# #显式定义 qconfig，避免 reduce_range 警告
# qconfig = quant.QConfig(
#     activation=quant.MinMaxObserver.with_args(quant_min=0, quant_max=255),
#     weight=quant.PerChannelMinMaxObserver.with_args(
#         quant_min=-128, quant_max=127, dtype=torch.qint8
#     )
# )
# model.qconfig = qconfig

# #准备量化
# quant.prepare(model, inplace=True)

# #用少量数据做 calibration
# transform = transforms.ToTensor()
# dataset = RawFaceDataset('att_faces.raw', transform=transform)
# loader = DataLoader(dataset, batch_size=32, shuffle=False)

# with torch.no_grad():
#     for imgs, _ in loader:
#         model(imgs)
#         break  #只跑一个 batch 用于校准

# #转换为量化模型
# quant.convert(model, inplace=True)

# #保存量化后的模型
# torch.save(model.state_dict(), 'mobilenetv2_face_quantized.pth')


import torch
from torch.ao.quantization import get_default_qconfig
from torch.ao.quantization.quantize_fx import prepare_fx, convert_fx
from torchvision import transforms
from dataset import RawFaceDataset
from model import MobileNetV2
from torch.utils.data import DataLoader

import torch
import torch.ao.quantization as quant
from model import MobileNetV2
from dataset import RawFaceDataset
from torchvision import transforms
from torch.utils.data import DataLoader

# 加载模型
model = MobileNetV2()
model.load_state_dict(torch.load('mobilenetv2_face.pth'))
model.eval()

# 设置 quant config，明确指定 quant_min 和 quant_max
model.qconfig = quant.QConfig(
    activation=quant.MinMaxObserver.with_args(quant_min=0, quant_max=255, dtype=torch.quint8),
    weight=quant.PerChannelMinMaxObserver.with_args(dtype=torch.qint8, qscheme=torch.per_channel_symmetric)
)

# 准备量化
quant.prepare(model, inplace=True)

# 准备校准数据（只做一次前向）
dataset = RawFaceDataset('att_faces.raw', transform=transforms.ToTensor())
loader = DataLoader(dataset, batch_size=32)

with torch.no_grad():
    for imgs, _ in loader:
        model(imgs)
        break  # 只需一批数据用于校准

# 转换为量化模型
quant.convert(model, inplace=True)

# 保存为量化后的 .pth
torch.save(model.state_dict(), 'mobilenetv2_face_quantized.pth')
print("量化模型已保存为 mobilenetv2_face_quantized.pth")

