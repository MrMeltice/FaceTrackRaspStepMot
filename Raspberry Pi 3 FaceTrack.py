from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import cv2

screenwidth = 480
screenheight = 320

try:
    GPIO.setmode(GPIO.BOARD)
    control_pins = [13,11,15,12]
    control_pinsNew = [35,36,37,38]       
    for pin in control_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
        
    for pinNew in control_pinsNew:
        GPIO.setup(pinNew, GPIO.OUT)
        GPIO.output(pinNew, 0)
        
    
        
    halfstep_seqL = [
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1],
    ]
    
    halfstep_seqR = [
        [1,0,0,1],
        [0,0,0,1],
        [0,0,1,1],
        [0,0,1,0],
        [0,1,1,0],
        [0,1,0,0],
        [1,1,0,0],
        [1,0,0,0],
    ]
    
    
    
    face_cascade = cv2.CascadeClassifier('/home/pi/openCV/data/haarcascade_frontalface_default.xml')
    
    camera = PiCamera()
    camera.resolution = (screenwidth, screenheight)
    camera.rotation = 180
    rawCapture = PiRGBArray(camera, size = (screenwidth, screenheight))
    
    time.sleep(0.1)

    
    for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):
        
        img = frame.array
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 230, 0), 2)
        
            roicolor = img[y:y+h,x:x+w]
            
            xmid = (screenwidth - w)/2
            
            hmid = (screenheight - h)/2
            
            if x > xmid + 15:
                print("movv leff")
                for i in range(1) :
                    for halfstep in range (8) :
                        for pin in range (4) :
                            GPIO.output(control_pins[pin], halfstep_seqL[halfstep][pin])
                        time.sleep(0.004)

            elif x < xmid - 15:
                print("movv righh")
                for i in range(1) :
                    for halfstep in range (8) :
                        for pin in range (4) :
                            GPIO.output(control_pins[pin], halfstep_seqR[halfstep][pin])
                        time.sleep(0.004)
                        
            if y > hmid + 15:
                print("movv UP")
                for i in range(1) :
                    for halfstep in range (8) :
                        for pin in range (4) :
                            GPIO.output(control_pinsNew[pin], halfstep_seqL[halfstep][pin])
                        time.sleep(0.004)

            elif y < hmid - 15:
                print("movv DOWN")
                for i in range(1) :
                    for halfstep in range (8) :
                        for pin in range (4) :
                            GPIO.output(control_pinsNew[pin], halfstep_seqR[halfstep][pin])
                        time.sleep(0.004)
            
    
            
            
            
        cv2.imshow("Frame", img)
        
        
        
        key = cv2.waitKey(1) & 0xFF
        
        rawCapture.truncate(0)
        
        if key == ord('q'):
            break
        
finally:
    cv2.destroyAllWindows()
    
    GPIO.cleanup()