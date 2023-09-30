from ultralytics import YOLO
import cv2
import cvzone
import math
import numpy as np
import time
import serial
cap = cv2.VideoCapture(0)
_, frame = cap.read()
rows, cols, _ = frame.shape
x_center=int(cols / 2)
y_center=int(rows/2)
def servo_angle_x(position_x):
    position_x=int(position_x*(180/cols))
    return (180-position_x)
def servo_angle_y(position_y):
    position_y = int(position_y * (180 / rows))
    return position_y

model = YOLO(r"E:\Downloads\best (2).pt")

classNames = ['Mature Areca Nuts', 'Semi-Mature Areca Nuts', 'Young Areca Nuts']
myColor = (0, 0, 255)
while True:
    success, img = cap.read()
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            #cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            x_mid = (x1 + x2) // 2
            y_mid = (y1 + y2) // 2
            break
    if boxes:
        # cvzone.cornerRect(img, (x1, y1, w, h))

        # Confidence
        conf = math.ceil((box.conf[0] * 100)) / 100
        # Class Name
        cls = int(box.cls[0])
        print(cls)
        currentClass = classNames[cls]
        print(currentClass)
        if conf > 0.5:
            if currentClass == 'Mature Areca Nuts':
                myColor = (0, 0, 255)
            elif currentClass == 'Semi-Mature Areca Nuts':
                myColor = (0, 255, 0)
            else:
                myColor = (255, 0, 0)

            cvzone.putTextRect(img, f'{classNames[cls]} {conf}',
                               (max(0, x1), max(35, y1)), scale=1, thickness=1, colorB=myColor,
                               colorT=(255, 255, 255), colorR=myColor, offset=5)
            cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 3)

            cv2.line(img, (x_mid, 0), (x_mid, 480), (0, 255, 0), 2)
            cv2.line(img, (y_mid, 0), (y_mid, 480), (0, 255, 0), 2)
            ser = serial.Serial('COM4', 115200, timeout=1)
            x1_medium = servo_angle_x(x_mid)
            y_medium = servo_angle_y(y_mid)

            command = [
                f'x1_medium={x1_medium}',
                f'y_medium={y_medium}'
            ]
            command_string = '&'.join(command)
            print(command_string)
            ser.write(command_string.encode() + b'\n')
            time.sleep(0.2)
            ser.close()




    cv2.imshow("Image", img)
    cv2.waitKey(1)
