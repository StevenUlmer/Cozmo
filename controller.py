#! /usr/bin/env python3
from pynput.keyboard import Key, KeyCode, Listener, Controller
#import cozmo as cozmo

class controller:
    def __init__(self, robot):
        self.robot = robot
        self.keyboard = Controller()
        self.lastKeyPress = None

    def startListener(self):
        print("called start")
        with Listener(on_release = self.on_key_release, on_press = self.on_key_press) as self.listener:
            self.listener.join()

    def stopListener(self):
        self.listener.stop()

    def on_key_release(self, key):
        self.lastKeyPress = None
        self.robot.stop_all_motors()
        if key == Key.esc:
            return False

    def on_key_press(self, key):
        self.listener.stop()
        if self.lastKeyPress == key: #or self.robot.has_in_progress_actions:
            return
        self.lastKeyPress = key
        #drive_wheel_motors(l_wheel_sporwarded, r_wheelspeed, l_wheel_acc=None, r_wheel_acc=None)
        if key==KeyCode.from_char('w') or key == Key.up:
            self.robot.drive_wheels(50.0, 50.0)  #drive forwards
        elif key==KeyCode.from_char('d') or key == Key.right:
            self.robot.drive_wheels(50.0, -50.0)  #turn right
        elif key==KeyCode.from_char('a') or key == Key.left:
            self.robot.drive_wheels(-50.0, 50.0)  #turn left
        elif key==KeyCode.from_char('s') or key == Key.down:
            self.robot.drive_wheels(-50.0, -50.0)  #go backwards
        elif key== KeyCode.from_char('t'):
            self.robot.move_lift(1.0) #raise lift
        elif key == KeyCode.from_char('r'):
            self.robot.move_lift(-1.0) #lower lift

##def Controller(robot: cozmo.robot.Robot):
##    controller = controller(robot)
##    print("press esc to exit")
##    print("use aswd or arrow keys to control the robot")
##    print("R will lower the lift and T will raise it")
##    print("Happy Driving!")
##    with Listener(on_release = on_key_release, on_press = on_key_press) as listener:
##        listener.join()

#cozmo.run_program(Controller)
controller = controller("")
controller.startListener()
controller.stopListener()
