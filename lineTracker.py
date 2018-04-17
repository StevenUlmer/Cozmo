import numpy as np
import cv2
import cozmo
from PIL import Image

def lineTracker(robot: cozmo.robot.Robot):
    video_capture = cv2.VideoCapture(-1)
    video_capture.set(3, 160)
    video_capture.set(4, 120)
    while(True):
        latest_image = robot.world.latest_image.raw_image
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
                    if cx >= 220:
                        robot.drive_wheels(10.0, -10.0)
                        print ("Turn Right!")
                    if cx < 220 and cx > 50:
                        robot.drive_wheels(15.0, 15.0)
                        print ("On Track!")
                    if cx <= 50:
                        robot.drive_wheels(-10.0, 10.0)
                        print ("Turn Left")
                else:
                    print ("I don't see the line")
            except:
                robot.stop_all_motors()
                
            #Display the resulting frame
            cv2.imshow('frame',crop_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


cozmo.run_program(lineTracker, use_viewer=True)
##cozmo.run_program(lineTracker)
