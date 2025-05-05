import cv2
import torch
from torchvision import transforms
from model import MobileNetV2

model = MobileNetV2()
model.load_state_dict(torch.load('mobilenetv2_face.pth'))
model.eval()

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (64, 64))
    tensor = transform(small).unsqueeze(0)
    with torch.no_grad():
        out = model(tensor)
        prob = torch.softmax(out, dim=1)[0,1].item()
    label = f"Face: {prob:.2f}" if prob > 0.5 else "No face"
    cv2.putText(frame, label, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow('Face Detection', frame)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()