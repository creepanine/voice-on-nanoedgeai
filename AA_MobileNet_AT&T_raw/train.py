import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from dataset import RawFaceDataset
from model import MobileNetV2

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

dataset = RawFaceDataset('att_faces.raw', transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

model = MobileNetV2()
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

model.train()
for epoch in range(20):
    for imgs, labels in dataloader:
        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

torch.save(model.state_dict(), 'mobilenetv2_face.pth')