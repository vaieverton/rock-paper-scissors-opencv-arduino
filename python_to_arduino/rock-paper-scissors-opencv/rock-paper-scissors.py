import cv2
import os
import time
import serial
import handTrackingModule as htm
import random

def getNumber(ar):
    s=""
    for i in ar:
       s+=str(ar[i]);
       
    if(s=="00000"):
        return (0)
    elif(s=="01000"):
        return(1)
    elif(s=="01100"):
        return(2)
    elif(s=="01110"):
        return(3)
    elif(s=="01111" or s=="11110"):
        return(4)
    elif(s=="11111"):
        return(5)    

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.1)
    # data = arduino.readline()
    # return data

wcam,hcam=640,480
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime=0
detector = htm.handDetector(detectionCon=0.75)

text = ""

number = -1

moves = ['pedra', 'tesoura', 'papel']

while True:
    success,img=cap.read()
    img = detector.findHands(img, draw=True )
    lmList=detector.findPosition(img,draw=False)
    tipId=[4,8,12,16,20]

    if(cv2.waitKey(1) & 0xFF == ord('p')):
        number = random.randint(0, 2)
        print(number)


    if(len(lmList)!=0):
        fingers=[]
        #thumb
        if(lmList[tipId[0]][1]>lmList[tipId[0]-1][1]):
                fingers.append(1)
        else :
                fingers.append(0)
        #4 fingers
        for id in range(1,len(tipId)):
            
            if(lmList[tipId[id]][2]<lmList[tipId[id]-2][2]):
                fingers.append(1)
            
            else :
                fingers.append(0)
        
        if (getNumber(fingers) == 2 and number == 0):
            text = moves[1]
            write_read('9')
        elif (getNumber(fingers) == 2 and number == 2):
            text = 'tesoura'
            textEnemy = 'papel'
            write_read('8')
        elif (getNumber(fingers) == 2 and number == 1):
            text = 'tesoura'
            textEnemy = 'tesoura'
            write_read('0')
        elif (getNumber(fingers) == 5 and number == 0):
            text = moves[2]
            write_read('8')
        elif (getNumber(fingers) == 5 and number == 1):
            text = moves[2]
            write_read('9')
        elif (getNumber(fingers) == 5 and number == 2):
            text = moves[2]
            write_read('0')
        elif (getNumber(fingers) == 0 and number == 1):
            text = moves[0]
            write_read('8')
        elif (getNumber(fingers) == 0 and number == 0):
            text = moves[0]
            write_read('0')
        elif (getNumber(fingers) == 0 and number == 2):
            text = moves[0]
            write_read('9')
        else:
            text = "???"
            write_read('0')
        cv2.putText(img,str(text),(45,375),cv2.FONT_HERSHEY_PLAIN,
                                     4,(0,255,0),10)  
        

    cTime=time.time()
    pTime=cTime

    textEnemy = moves[number]
    
    if number != -1:
        cv2.putText(img,str(textEnemy),(345,375),cv2.FONT_HERSHEY_PLAIN,
                                     4,(0,0,255),10)  
    

    cv2.imshow("image",img)

    if(cv2.waitKey(1) & 0xFF== ord('q')):
        break


