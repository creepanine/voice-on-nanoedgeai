# infer_local.py
import torch
import cv2
from torchvision import transforms
from model import MobileNetV2

def main():
    # 1. 加载模型
    model = MobileNetV2()
    model.load_state_dict(torch.load('mobilenetv2_face.pth', map_location='cpu'))
    model.eval()

    # 2. 图像预处理变换
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    # 3. 加载原始彩色图用于显示，灰度图用于检测
    img_color = cv2.imread('test/test2.jpg')
    if img_color is None:
        print("无法加载图片 test/test2.jpg")
        return
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    # 4. 人脸检测
    casc_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(casc_path)
    faces = face_cascade.detectMultiScale(
        img_gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # 5. 对每个检测到的人脸区域进行识别，并绘制矩形框和概率
    for (x, y, w, h) in faces:
        # 裁剪人脸并转换为模型输入
        face_roi = img_gray[y:y+h, x:x+w]
        face_resized = cv2.resize(face_roi, (64, 64))
        tensor = transform(face_resized).unsqueeze(0)  # [1,1,64,64]

        # 模型推理
        with torch.no_grad():
            output = model(tensor)
            prob = torch.softmax(output, dim=1)[0, 1].item()

        # 绘制框和文字（用绿色框）
        label = f"{prob:.2f}"
        cv2.rectangle(img_color, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            img_color, label, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
        )

    # 6. 显示结果
    cv2.imshow('Face Detection', img_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

