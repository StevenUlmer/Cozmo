import random
import cozmo as cozmo
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
import time
from PIL import Image, ImageDraw, ImageFont
from cozmo.util import distance_mm, speed_mmps, degrees

def Cozmogram(robot: cozmo.robot.Robot):
    global Robot
    global faceForwardAngle
    Robot = robot
    faceForwardAngle = Robot.pose_angle.degrees
    print(Robot.pose.position)
##    moveCube(3, 50, 'left')
##    moveCube(1, 50, 'left')
##    moveCube(2, 50, 'left')
    totalGames = 0
    wins = 0
    Robot.set_lift_height(0).wait_for_completed()
    while(True):
        originalCubeOrder = getCubeListOrder()
        wordList = ["yes", "gag", "egg", "ace", "age", "all", "air", "gal", "lag", "mom", "leg", "gel", "beg", "cop", "cry", "cut", "did", "dug", "few", "ego", "fan", "foe", "fin", "gym", "hip"]
        originalWord = wordList[random.randint(0,len(wordList)-1)]
        originalWord = "fan"
        shuffledWord = shuffleWord(originalWord)
        originalCubeOrder = assignCubesLetters(originalCubeOrder, shuffledWord)
        wait(shuffledWord, wins, totalGames)
        finalCubeOrder = getCubeListOrder()
        finalCubeOrder = assignCubeLettersFromOriginalCubes(originalCubeOrder, finalCubeOrder)
        print(finalCubeOrder)
        if(checkIfCorrect(finalCubeOrder, wordList)):
            win()
            wins += 1
        else:
##            lose()
            fixCubes(robot, finalCubeOrder, originalWord)
        totalGames += 1

def wait(oldWord, wins, totalGames):
    for i in range(2):
        word = oldWord + " " + str(10-i)
        displayWordOnScreen(word, 1000.0, wins, totalGames)
        time.sleep(2)

def getCubeListOrder():
    global Robot
    cube1 = Robot.world.get_light_cube(LightCube1Id)
    cube2 = Robot.world.get_light_cube(LightCube2Id)
    cube3 = Robot.world.get_light_cube(LightCube3Id)
##    cube1.set_lights(cozmo.lights.red_light)
##    cube2.set_lights(cozmo.lights.green_light)
##    cube3.set_lights(cozmo.lights.blue_light)
    cubes = [{"cubeId": 1, "position": cube1.pose.position.y, "x": cube1.pose.position.x}, {"cubeId": 2, "position": cube2.pose.position.y, "x": cube2.pose.position.x}, {"cubeId": 3, "position": cube3.pose.position.y, "x": cube3.pose.position.x}]
    cubes.sort(key=lambda x: x["position"], reverse=False)
    return cubes

def displayWordOnScreen(word, time, wins, totalGames):
    global Robot
    font = getFont(18)
    textImage = make_text_image(word, 6, 0, font=font, text_image=None)
    winsOverGames = "Correct: " + str(wins) + "/" + str(totalGames)
    font = getFont(12)
    textImage = make_text_image(winsOverGames, 6, 18, font=font, text_image=textImage)
    
    image_data = cozmo.oled_face.convert_image_to_screen_data(textImage)

    # display for 1 second
    Robot.display_oled_face_image(image_data, time)

def getFont(size):
    font = None
    try:
        font = ImageFont.truetype("arial.ttf", size)
    except IOError:
        try:
            font = ImageFont.truetype("/Library/Fonts/Arial.ttf", size)
        except IOError:
            pass
    return font

def assignCubesLetters(cubeList, word):
    for i in range(len(word)):
        cubeList[i]["letter"] = word[i]
    return cubeList

def assignCubeLettersFromOriginalCubes(originalCubeList, afterCubeList):
    for i in range(3):
        letter = originalCubeList[i]["letter"]
        cubeId = originalCubeList[i]["cubeId"]
        for j in range(3):
            if afterCubeList[j]["cubeId"] == cubeId:
                afterCubeList[j]["letter"] = letter
                break
    return afterCubeList

def checkIfCorrect(finalCubeOrder, correctWordsList):
    if len(finalCubeOrder) != 3:
        return false
    word = ""
    for i in range(3):
        word += finalCubeOrder[i]["letter"]
    if word in correctWordsList:
        return True
    return False

def shuffleWord(originalWord):
    return "afn"
    word = list(originalWord)
    random.shuffle(word)
    word = ''.join(word)
    if(word == originalWord):
       return shuffleWord(word)
    return word

def make_text_image(text_to_draw, x, y, font=None, text_image=None):
    if text_image == None:
        text_image = Image.new('RGBA', cozmo.oled_face.dimensions(), (0, 0, 0, 255))
    dc = ImageDraw.Draw(text_image)
    dc.text((x, y), text_to_draw, fill=(255, 255, 255, 255), font=font)
    return text_image


def win():
    global Robot
    time.sleep(1)
    Robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabWin, ignore_body_track=True).wait_for_completed()
    time.sleep(3)

def lose():
    global Robot
    time.sleep(1)
    Robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabLose, ignore_body_track=True).wait_for_completed()
    time.sleep(3)

def fixCubes(robot, cubeOrder, originalWord):
## keep same position on table if possible    
    if originalWord[0] == cubeOrder[0]["letter"]:
        print("0, 2, 1")
        moveCube(cubeOrder[1]["cubeId"], cubeOrder[1]["x"], cubeOrder[1]["position"]+110)
        moveCube(cubeOrder[0]["cubeId"], cubeOrder[0]["x"], cubeOrder[0]["position"]+55)
##        move cubeOrder[1] to cubeOrder[2]+50
##        move cubeOrder[0] to cubeOrder[2]-50
    elif originalWord[1] == cubeOrder[0]["letter"]:
        if originalWord[2] == cubeOrder[1]["letter"]:
            print("2, 0, 1")
            moveCube(cubeOrder[2]["cubeId"], cubeOrder[2]["x"], cubeOrder[2]["position"]-165)
##            move cubeOrder[2] to cubeOrder[0]-50
        else:
            print("1, 0, 2")
            moveCube(cubeOrder[1]["cubeId"], cubeOrder[1]["x"], cubeOrder[1]["position"]-110)
            moveCube(cubeOrder[2]["cubeId"], cubeOrder[2]["x"], cubeOrder[2]["position"]-55)
##            move cubeOrder[1] to cubeOrder[0]-50
##            move cubeOrder[2] to cubeOrder[0]+50
    else:
        if originalWord[0] == cubeOrder[1]["letter"]:
            print("1, 2, 0")
            moveCube(cubeOrder[0]["cubeId"], cubeOrder[0]["x"], cubeOrder[0]["position"]+165)
##            move cubeOrder[0] to cubeOrder[2]+50
        else:
            print("2, 1, 0")
            moveCube(cubeOrder[1]["cubeId"], cubeOrder[1]["x"], cubeOrder[1]["position"]+110)
            moveCube(cubeOrder[0]["cubeId"], cubeOrder[0]["x"], cubeOrder[0]["position"]+220)
##            move cubeOrder[1] to cubeOrder[2]+50
##            move cubeOrder[0] to cubeOrder[2]+100

    pass

def moveCube(cubeId, x, y):
    dockWithCube(cubeId)
    moveCubeTo(x, y)

def dockWithCube(cubeId):
    global Robot
    cube1 = Robot.world.get_light_cube(LightCube1Id)
    cube2 = Robot.world.get_light_cube(LightCube2Id)
    cube3 = Robot.world.get_light_cube(LightCube3Id)
    if cubeId == 1:
        cube = cube1
    elif cubeId == 2:
        cube = cube2
    else:
        cube = cube3
    print(cube)
    Robot.dock_with_cube(cube).wait_for_completed()

def moveCubeTo(x, y):
    global Robot
    global faceForwardAngle
    speed = speed_mmps(50)
    pickUpX = Robot.pose.position.x
    Robot.set_lift_height(1).wait_for_completed()
    Robot.drive_straight(distance_mm(-100), speed, False).wait_for_completed()
    print(Robot.pose.position)
    if Robot.pose.position.y > y:
        turnRight(faceForwardAngle, y, speed)
    else:
        turnLeft(faceForwardAngle, y, speed)
    Robot.drive_straight(distance_mm(100), speed, False).wait_for_completed()
##    while Robot.pose.position.x < pickUpX:
##        print(Robot.pose.position.x, pickUpX)
##        Robot.drive_straight(distance_mm(5), speed, False).wait_for_completed()
    Robot.set_lift_height(0).wait_for_completed()
    Robot.drive_straight(distance_mm(-150), speed, False).wait_for_completed()

def turnRight(faceForwardAngle, y, speed):
    print(Robot.pose_angle.degrees)
    Robot.turn_in_place(degrees(-80)).wait_for_completed()
    while Robot.pose_angle.degrees > faceForwardAngle-90:
        Robot.turn_in_place(degrees(-5)).wait_for_completed()
    print(Robot.pose_angle.degrees)
    while Robot.pose.position.y > y:
        print(Robot.pose.position.y)
        print(y)
        Robot.drive_straight(distance_mm(5), speed, False).wait_for_completed()
    Robot.turn_in_place(degrees(80)).wait_for_completed()
    while Robot.pose_angle.degrees < faceForwardAngle:
        Robot.turn_in_place(degrees(5)).wait_for_completed()

def turnLeft(faceForwardAngle, y, speed):
    print(Robot.pose_angle.degrees)
    Robot.turn_in_place(degrees(80)).wait_for_completed()
    while Robot.pose_angle.degrees < faceForwardAngle+90:
        Robot.turn_in_place(degrees(5)).wait_for_completed()
    print(Robot.pose_angle.degrees)
    while Robot.pose.position.y < y:
        print(Robot.pose.position.y)
        print(y)
        Robot.drive_straight(distance_mm(5), speed, False).wait_for_completed()
    Robot.turn_in_place(degrees(-80)).wait_for_completed()
    while Robot.pose_angle.degrees > faceForwardAngle:
        Robot.turn_in_place(degrees(-5)).wait_for_completed()

cozmo.run_program(Cozmogram)
