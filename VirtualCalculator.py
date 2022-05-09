import cv2
from cv2 import CAP_DSHOW
from cvzone.HandTrackingModule import HandDetector
 
 
class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
 
    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (150,150,150), cv2.FILLED)  #bg color
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (180,180,180), 3) #rect color
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN,
                    2, (0,0,222), 2)
 
    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, (self.pos[0] + 3, self.pos[1] + 3),
                          (self.pos[0] + self.width - 3, self.pos[1] + self.height - 3),
                          (255, 255, 255), cv2.FILLED)
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)
            return True
        else:
            return False
 
 
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]



buttonList = []


for x in range(4):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150
 
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

myEquation = ''
delayCounter = 0
cap = cv2.VideoCapture(0,CAP_DSHOW)
detector = HandDetector(detectionCon=0.8, maxHands=1)
 
 
 
while True:
    success, img = cap.read()
    img=cv2.resize(img,(1280,1080))
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    for button in buttonList:
        button.draw(img)
 
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8], lmList[12], img)
        print(length)
        x, y = lmList[8]
        
        # for checking whic button is clicked 
        if length < 50 and delayCounter == 0:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y):
                    myValue = buttonListValues[int(i % 4)][int(i / 4)]  # get correct number
                    if myValue == '=':
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue
                    delayCounter = 1
                    
                    
 #for avoiding multiple clcks
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0


    cv2.putText(img, myEquation, (810, 130), cv2.FONT_HERSHEY_PLAIN,3, (0, 0, 0), 3)
    cv2.imshow("Image", img)
    if ord('q')==cv2.waitKey(1):
        break