# Utils.py

from ev3dev2.sound import Sound 
from ev3dev2.display import Display
from ev3dev2.button import Button
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2._platform.ev3 import INPUT_1, INPUT_2, INPUT_3, INPUT_4 

"""
The Utils class handles the basic input from sensors and the output through speech, beeps and displays.
"""
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
            print(string)
            self.__s.speak(string, volume=50, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            
    def mBeep(self):
        if self.__playDebugSound:
            self.__s.beep(play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            
    """
    Tries to update the cached sensor values. 
    @param quick: [only relevant for master brick] boolean describes whether the update should be as quick as possible or not 
    """
    def updateSensorVals(self, quick = True):
        if self.__mode == 1:
            # first check for button:
            self.lastBtns = self.btn.any()
            
            self.lastColorL = self.colorL.color
            self.lastColorC = self.colorM.color
            self.lastColorR = self.colorR.color
            if not quick: 
                self.lastDistB = self.usSensorB.distance_centimeters
                # TODO: request update from slave
                print("MASTER: Requesting sensor readings")
                self.__sock_out.write("{'stop': False, 'dataRequest': True}\n")
                self.__sock_out.flush()
        else: # __mode is 2
            self.lastTouchL = self.touchL.is_pressed
            self.lastTouchR = self.touchR.is_pressed
            self.lastTouchB = self.touchB.is_pressed
            self.lastDistF = self.usSensorF.distance_centimeters     
    
    
    """
        Initialise
        @param mode: 1 if brick1, 2 if brick2; master brick is 1
        @param sock_out, must be specified if mode=1. It is the socket directed to the slave brick.
    """ 
    def __init__(self, mode, sock_out = None):
        self.__mode = mode
        self.__sock_out = sock_out
        if mode == 1 and sock_out == None:
            raise Exception("sock_out should be specified in master mode!")
        
        self.__playDebugSound = False
        self.__s = Sound()
        
        self.display = Display()
        self.display.clear()
        
        if self.__mode == 1: # brick 1
            self.btn = Button()
            
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
        self.lastColorC = 0
        self.lastColorR = 0
        self.lastDistB = 0
        self.lastTouchL = False
        self.lastTouchR = False
        self.lastTouchB = False
        self.lastBtns = False
        self.lastDistF = 0
        
        self.isDone = False # Set to True if the system should terminate
            
        
        
        
        
        
        
        
        
        
        