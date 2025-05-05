# import torch.nn as nn
# from torchvision.models import mobilenet_v2

# class MobileNetV2(nn.Module):
#     def __init__(self, num_classes=2):
#         super().__init__()
#         self.model = mobilenet_v2(width_mult=0.25)
#         self.model.features[0][0] = nn.Conv2d(1, self.model.features[0][0].out_channels,
#                                               kernel_size=3, stride=2, padding=1, bias=False)
#         self.model.classifier[1] = nn.Linear(self.model.classifier[1].in_features, num_classes)

#     def forward(self, x):
#         return self.model(x)

import torch.nn as nn
from torchvision.models import mobilenet_v2
import torch.ao.quantization as quant
import torch

class MobileNetV2(nn.Module):
    def __init__(self, num_classes=2):
        super().__init__()
        self.quant = quant.QuantStub()
        self.dequant = quant.DeQuantStub()
        self.model = mobilenet_v2(width_mult=0.25)
        self.model.features[0][0] = nn.Conv2d(1, self.model.features[0][0].out_channels,
                                              kernel_size=3, stride=2, padding=1, bias=False)
        self.model.classifier[1] = nn.Linear(self.model.classifier[1].in_features, num_classes)

    def forward(self, x):
        x = self.quant(x)
        x = self.model(x)
        x = self.dequant(x)
        return x
