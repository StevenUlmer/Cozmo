from pynput.keyboard import Key, KeyCode, Listener
import cozmo as cozmo
from math import sqrt
import time
import numpy as np
import cv2
from PIL import Image
import threading

class autoDrive:
    def __init__(self, robot: cozmo.robot.Robot):
        self.robot = robot
        self.lastKeyPress = None
        self.lastKnownDirection = None

    def startListener(self):
        with Listener(on_release = self.on_key_release, on_press = self.on_key_press) as self.listener:
            self.listener.join()

    def startDriving(self):
        self.startListener()

    def on_key_release(self, key):
        self.lastKeyPress = None
        self.robot.stop_all_motors()
        if key == Key.esc:
            return False
        elif key == KeyCode.from_char('f'):
            self.t = threading.Thread(target=self.autoDrive)
            self.t.start()
            
    def on_key_press(self, key):
        if self.lastKeyPress == key or self.robot.has_in_progress_actions:
            return
        self.lastKeyPress = key
        if key==KeyCode.from_char('w') or key == Key.up:
            if hasattr(self, 't'):
                self.t.auto_driving = False
            self.robot.drive_wheels(50.0, 50.0)  #drive forwards
        elif key==KeyCode.from_char('d') or key == Key.right:
            if hasattr(self, 't'):
                self.t.auto_driving = False
            self.robot.drive_wheels(50.0, -50.0)  #turn right
        elif key==KeyCode.from_char('a') or key == Key.left:
            if hasattr(self, 't'):
                self.t.auto_driving = False
            self.robot.drive_wheels(-50.0, 50.0)  #turn left
        elif key==KeyCode.from_char('s') or key == Key.down:
            if hasattr(self, 't'):
                self.t.auto_driving = False
            self.robot.drive_wheels(-50.0, -50.0)  #go backwards
        elif key== KeyCode.from_char('t'):
            self.robot.move_lift(1.0) #raise lift
        elif key == KeyCode.from_char('r'):
            self.robot.move_lift(-1.0) #lower lift
            

    def autoDrive(self):
        t = threading.currentThread()
        while(getattr(t, "auto_driving", True)):
            latest_image = self.robot.world.latest_image.raw_image
            if latest_image is not None:
                latest_image = np.array(latest_image)
                # Capture the frames
                frame = latest_image

                # Crop the image
                crop_img = frame[60:120, 0:320]

                # Convert to grayscale
                gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

                # Gaussian blur
                blur = cv2.GaussianBlur(gray,(5,5),0)

                # Color thresholding
                ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

                # Erode and dilate to remove accidental line detections
                mask = cv2.erode(thresh, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)

                # Find the contours of the frame
                img, contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

                # Find the biggest contour (if detected)
                try:
                    if len(contours) > 0:
                        c = max(contours, key=cv2.contourArea)
                        M = cv2.moments(c)
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
                        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
                        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
                        leftWheelSpeed = self.calcLeft(cx)
                        rightWheelSpeed = self.calcRight(cx)
                        if leftWheelSpeed < 25:
                            self.lastKnownDirection = "left"
                        elif rightWheelSpeed < 25:
                            self.lastKnownDIrection = "right"
                        self.robot.drive_wheels(leftWheelSpeed, rightWheelSpeed)
                        time.sleep(.25)
                    else:
                        if self.lastKnownDirection == "right":
                            self.turnRight()
                        elif self.lastKnownDirection == "left":
                            self.turnLeft()
                        else:
                            print ("I'm failing. Please take over")
                except:
                    print("failing")
                    self.robot.stop_all_motors()

                cv2.imshow('frame',crop_img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    def calcLeft(self, x):
        if x >= 160:
            return 25
        else:
            return -1*(25-(50*(x/160)))

    def calcRight(self, x):
        if x <= 160:
            return 25
        else:
            return 25-50*((x-160)/160)

    def turnRight(self):
        self.robot.drive_wheels(15, -15)

    def turnLeft(self):
        self.robot.drive_wheels(-15, 15)

def AutoDrive(robot: cozmo.robot.Robot):
    autoDriveing = autoDrive(robot)
    autoDriveing.startDriving()

cozmo.run_program(AutoDrive, use_viewer=True)

