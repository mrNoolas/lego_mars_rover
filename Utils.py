# Utils.py

from ev3dev2.sound import Sound 
from ev3dev2.display import Display
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2._platform.ev3 import INPUT_1, INPUT_2, INPUT_3, INPUT_4 

class Utils:
    def int2SpeakColor(self, colornr):
        if colornr == 0:
            #print("NoColor")
            self.mSpeak('This is not a color')
        elif colornr == 1:
            #print("Black")
            self.mSpeak('Black')
        elif colornr == 2:
            #print("Blue")
            self.mSpeak('Blue')
        elif colornr == 3:
            #print("Green")
            self.mSpeak('Green')
        elif colornr == 4:
            #print("Yellow")
            self.mSpeak('Yellow')
        elif colornr == 5:
            #print("Red")
            self.mSpeak('Red')
        elif colornr == 6:
            #print("White")
            self.mSpeak('White')
        elif colornr == 7:
            #print("Brown")
            self.mSpeak('Brown')
        else:
            #print("No valid value") 
            self.mSpeak('Value not valid!')
                       
    # Moderated speech
    def mSpeak(self, string):
        if self.__playDebugSound:
            #print(string)
            self.__s.speak(string, volume=50, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            
    def mBeep(self):
        if self.__playDebugSound:
            self.__s.beep(play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            
    """
    tries to update the cached sensor values. 
    @param quick boolean describes whether the update should be as quick as possible or not
    """
    def updateSensorVals(self, quick = False):
        if self.__mode == 1:
            self.lastColorL = self.colorL.color
            self.lastColorM = self.colorM.color
            self.lastColorR = self.colorR.color
            if not quick:
                self.lastDistB = self.usSensorB.distance_centimeters
                # TODO: request update from slave
        else: # __mode is 2
            self.lastTouchL = self.touchL.is_pressed
            self.lastTouchR = self.touchR.is_pressed
            self.lastTouchB = self.touchB.is_pressed
            self.lastDistF = self.usSensorF.distance_centimeters
                
    # ========== Higher level vital functions ==========
    def onBorder(self):
        color = self.checkColor()
        return color == 1 or color == 0        
    
            
    def __init__(self, mode):
        self.__mode = mode
        
        self.__playDebugSound = False
        self.__s = Sound()
        
        self.display = Display()
        self.display.clear()
        
        if self.__mode == 1: # brick 1
            self.colorL = ColorSensor(INPUT_1)
            self.colorM = ColorSensor(INPUT_2)
            self.colorR = ColorSensor(INPUT_3)
        
            self.usSensorB = UltrasonicSensor(INPUT_4)
        else: # brick 2
            self.touchB = TouchSensor(INPUT_1)
            self.touchL = TouchSensor(INPUT_2)
            self.touchR = TouchSensor(INPUT_3)
            
            self.usSensorF = UltrasonicSensor(INPUT_4) 
                
        self.lastColorL = 0
        self.lastColorM = 0
        self.lastColorR = 0
        self.lastDistB = 0
        self.lastTouchL = False
        self.lastTouchR = False
        self.lastTouchB = False
        self.lastDistF = 0
        
        self.isDone = False # Set to True if the system should terminate
            
        
        
        
        
        
        
        
        
        
        