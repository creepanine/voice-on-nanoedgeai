import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from preprocess import load_and_preprocess_data
from model import create_model
import numpy as np

# 加载和预处理数据
X_train, X_test, y_train, y_test = load_and_preprocess_data('fer2013.csv')

# 转换为 PyTorch 数据集和 DataLoader
train_dataset = torch.utils.data.TensorDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.long))
test_dataset = torch.utils.data.TensorDataset(torch.tensor(X_test, dtype=torch.float32), torch.tensor(y_test, dtype=torch.long))

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

# 创建模型
model = create_model()
model = model.cuda()  # 如果有 GPU 可用

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 早停机制
class EarlyStopping:
    def __init__(self, patience=10, restore_best_weights=True):
        self.patience = patience
        self.restore_best_weights = restore_best_weights
        self.best_loss = np.inf
        self.best_model_state = None
        self.counter = 0

    def step(self, val_loss, model):
        if val_loss < self.best_loss:
            self.best_loss = val_loss
            self.best_model_state = model.state_dict()
            self.counter = 0
        else:
            self.counter += 1

        if self.counter >= self.patience:
            if self.restore_best_weights:
                model.load_state_dict(self.best_model_state)
            return True  # 触发早停
        return False

# 初始化早停
early_stopping = EarlyStopping(patience=10, restore_best_weights=True)

# 训练模型
epochs = 50
for epoch in range(epochs):
    model.train()
    train_loss = 0.0
    for data, target in train_loader:
        data, target = data.cuda(), target.cuda()
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()

    # 验证模型
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.cuda(), target.cuda()
            output = model(data)
            loss = criterion(output, target)
            val_loss += loss.item()

    print(f"Epoch {epoch + 1}/{epochs}, Train Loss: {train_loss / len(train_loader):.4f}, Val Loss: {val_loss / len(test_loader):.4f}")

    # 检查早停条件
    if early_stopping.step(val_loss / len(test_loader), model):
        print("早停触发，停止训练")
        break

# 保存模型
torch.save(model.state_dict(), 'saved_model/emotion_model.pth')
print("模型已保存至 'saved_model/emotion_model.pth'")