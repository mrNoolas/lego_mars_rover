# Utils.py

from ev3dev2.sound import Sound 
from ev3dev2.display import Display
from ev3dev2.button import Button
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2._platform.ev3 import INPUT_1, INPUT_2, INPUT_3, INPUT_4 
import time
from pyglet.resource import location

"""
The Utils class handles the basic input from sensors and the output through speech, beeps and displays.
"""
class Utils:
    def int2RetColor(self, colornr):
        if colornr == 0:
            return 'This is not a color'
        elif colornr == 1:
            return 'Black'
        elif colornr == 2:
            return 'Blue'
        elif colornr == 3:
            return 'Green'
        elif colornr == 4:
            return 'Yellow'
        elif colornr == 5:
            return 'Red'
        elif colornr == 6:
            return 'White'
        elif colornr == 7:
            return 'Brown'
        else:
            return 'Value not valid!'
    
    def int2SpeakColor(self, colornr):
        self.mSpeak(self.int2RetColor(colornr))
                       
    # Moderated speech
    def mSpeak(self, string):
        print(string)
        if self.__playDebugSound:
            self.__s.speak(string, volume=50, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            
    def mBeep(self):
        if self.__playDebugSound:
            self.__s.beep(play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
          
            
    # ========== Sensor handling ==========
    def updateSensorVals(self, quick = True):
        """
        Tries to update the cached sensor values. 
        @param quick: [only relevant for master brick] boolean describes whether the update should be as quick as possible or not 
        """
        if self.__mode == 1:
            # first check for button:
            self.lastBtns = self.btn.any()
            
            # only update the color if it is a valid one. Errors are assumed to be corrected with a future measurement
            if self.colorL.color != ColorSensor.COLOR_NOCOLOR: self.lastColorL = self.colorL.color
            if self.colorC.color != ColorSensor.COLOR_NOCOLOR: self.lastColorC = self.colorC.color
            if self.colorR.color != ColorSensor.COLOR_NOCOLOR: self.lastColorR = self.colorR.color
            
            # Updates the colors that were found. Assumes sensor values in utils are up to date.
            if self.lastColorL not in self.__colorsFoundL:
                self.__colorsFoundL.add(self.lastColorL)
            if self.lastColorR not in self.__colorsFoundR:
                self.__colorsFoundR.add(self.lastColorR)
            if self.lastColorC not in self.__colorsFoundC:
                self.__colorsFoundC.add(self.lastColorC)
            
            if not quick: 
                self.lastDistB = self.usSensorB.distance_centimeters
                # request update from slave
                self.__sock_out.write("{'stop': False, 'dataRequest': True}\n")
                self.__sock_out.flush()
        else: # __mode is 2
            self.lastTouchL = self.touchL.is_pressed
            self.lastTouchR = self.touchR.is_pressed
            self.lastTouchB = self.touchB.is_pressed
            self.lastDistF = self.usSensorF.distance_centimeters * 10   # give distance in mm
                    
    
    def wereColorsFound(self, targets, colors, cnd):
        """
        Checks whether the specified colors were found by the sensors in targets.
            @param targets: the sensors that should be checked for occurrences of 'colors'
            @param colors: the colors that must be present
            @return: True if the 'targets' together found all in 'colors'. False otherwise
        """
        colorsFound = set()
        if "left" in targets:
            colorsFound.update(self.__colorsFoundL)
        if "right" in targets:
            colorsFound.update(self.__colorsFoundR)
        if "center" in targets:
            colorsFound.update(self.__colorsFoundC)
        
        return colors.issubset(colorsFound)
    
    def startTimer(self):
        self.__startOfTimer = time.time()
    
    def didTimeExpire(self, interval, cnd):
        return time.time() - self.__startOfTimer >= interval
    
    def areSensorsTouched(self, sensors, value):
        """
        Checks whether the touch 'sensors' have 'value' as current status
            @param sensors: the sensors to check
            @param value: True or False as desired
            @return: True if all specified sensors have the desired value. False otherwise.
        """ 
        matchingValue = set()
        if self.lastTouchL == value:
            matchingValue.add("frontLeft")
        if self.lastTouchR == value:
            matchingValue.add("frontRight")
        if self.lastTouchB == value:
            matchingValue.add("back")
            
        return sensors.issubset(matchingValue)
    
    def resetTracker(self):
        self.__colorsFoundR = set()
        self.__colorsFoundL = set()
        self.__colorsFoundC = set()
        self.__startOfTimer = 0  
        
    def colorSensorOnBorder(self, borderColor = None):
        if borderColor == None: # any non black color will do
            return self.lastColorL != ColorSensor.COLOR_BLACK or self.lastColorC != ColorSensor.COLOR_BLACK or self.lastColorR != ColorSensor.COLOR_BLACK
        return self.lastColorL == borderColor or self.lastColorC == borderColor or self.lastColorR == borderColor
    
    # ========== Extra's ==========
    def reportInvalidState(self, location = "", message = ""):
        report = "Encountered invalid state"
        if location != "":
            report += " at " + location
        report += "."
        
        if message != "":
            report += " " + message
        
        print(report)
        print("The robot may be in an invalid location. Therefore it is shutting down.")
        
        self.shouldStop = True
     
    def __init__(self, mode, sock_out = None):
        """
        Initialise
        @param mode: 1 if brick1, 2 if brick2; master brick is 1
        @param sock_out, must be specified if mode=1. It is the socket directed to the slave brick.
        """
        self.__mode = mode
        self.__sock_out = sock_out
        
        if mode == 1 and (sock_out == None):
            raise Exception("sock_out should be specified in master mode!")
        
        self.__playDebugSound = False
        self.__s = Sound()
        
        self.display = Display()
        self.display.clear()
        
        if self.__mode == 1: # brick 1
            self.btn = Button()
            
            self.colorL = ColorSensor(INPUT_1)
            self.colorC = ColorSensor(INPUT_2)
            self.colorR = ColorSensor(INPUT_3)
        
            self.usSensorB = UltrasonicSensor(INPUT_4)
            
            self.resetTracker()
        else: # brick 2
            self.touchB = TouchSensor(INPUT_1)
            self.touchL = TouchSensor(INPUT_2)
            self.touchR = TouchSensor(INPUT_3)
            
            self.usSensorF = UltrasonicSensor(INPUT_4) 
                
        self.lastColorL = 0
        self.lastColorC = 0
        self.lastColorR = 0
        self.lastDistB = 20
        self.lastTouchL = False
        self.lastTouchR = False
        self.lastTouchB = False
        self.lastBtns = False
        self.lastDistF = 2550
        
        self.shouldStop = False # Set to True if the system should terminate
            
        
        
        
        
        
        
        
        
        
        