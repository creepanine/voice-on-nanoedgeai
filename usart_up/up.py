import cv2
import serial
import numpy as np
import time

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
small = cv2.resize(gray, (64,64))

# 配置串口参数
ser = serial.Serial(
    port='COM10',  # 串口号，根据实际情况修改
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# 发送数据
def send_data(data):
    ser.write(data)
    ser.flush()
    time.sleep(0.01)

# 接收数据
def read_data():
    data = ser.readline()
    try:
        # 先尝试直接解码为字符串
        return data.decode('utf-8').strip()
    except UnicodeDecodeError:
        # 如果不能解码，则返回十六进制字符串
        return data.hex()

data_array = np.array(small, dtype=np.uint8)
flattened_data = data_array.flatten().tobytes()

print(len(flattened_data)) 

#print("前20个字节（十进制）：", list(flattened_data[:20]))
#print("前20个字节（十六进制）：", [hex(x) for x in flattened_data[:20]])

send_data(flattened_data)

print("开始持续接收STM32数据，按Ctrl+C退出：")
try:
    while True:
        received = read_data()
        if received:  # 有数据才打印
            print("Received from STM32:", received)
except KeyboardInterrupt:
    print("接收结束。")
finally:
    ser.close()