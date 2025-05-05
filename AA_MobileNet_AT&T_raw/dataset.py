import torch
from torch.utils.data import Dataset
import numpy as np

class RawFaceDataset(Dataset):
    def __init__(self, raw_file, transform=None):
        self.imgs = []
        with open(raw_file, 'rb') as f:
            data = f.read()
        bits = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
        bits = bits.reshape(-1, 64, 64)
        self.imgs = [img.astype(np.uint8)*255 for img in bits]
        self.transform = transform

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        img = self.imgs[idx]
        label = 1  # 全为正样本
        if self.transform:
            img = self.transform(img)
        return img, label