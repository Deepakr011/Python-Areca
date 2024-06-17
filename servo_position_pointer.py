import time
import sys
import utime
from servo import Servo
import re 
led=machine.Pin(0,machine.Pin.OUT)
s1 = Servo(1)       # Servo pin is connected to GP0
s2=Servo(2)
def servo_Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
def servo_Angle1(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    s1.goto(round(servo_Map(angle,0,180,0,1024))) # Convert range value to angle value
def servo_Angle2(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    s2.goto(round(servo_Map(angle,0,180,0,1024)))    
while True:
    received_data = sys.stdin.readline().strip()
    if received_data:
        led.on()
        x1_match = re.search(r'x1_medium=(\d+)', received_data)
        y_match = re.search(r'y_medium=(\d+)', received_data)
        if x1_match and y_match:
            x1_medium = int(x1_match.group(1))
            y_medium = int(y_match.group(1))
            servo_Angle1(x1_medium)
            servo_Angle2(y_medium)
    else:
        led.off()
         
    

        
        
              
 

