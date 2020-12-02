# MovementController.py

from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedRPS, SpeedPercent, LargeMotor
from time import sleep
import random

class MovementController:
    #========== Probe movement ==========
    def probe(self):
        raise NotImplementedError
    
    # ========== basic movements ==========
    def rotate(self, direction, rotations, condFuncs):
        raise NotImplementedError
    
    def forward(self, rotations, condFuncs):
        raise NotImplementedError
    
    def backward(self, rotations, condFuncs):
        raise NotImplementedError
    
    def turn(self, turnCircleDiameter, angle, condFuncs):
        raise NotImplementedError
    
    
    # ========== border aware movements ==========
    def __findBorder(self, direction, rotations = 0, condFuncs):
        raise NotImplementedError
    
    def alignWithBorder(self, condFuncs):
        raise NotImplementedError
    
    def alignWithPond(self, condFuncs):
        raise NotImplementedError
    
    def __onBorderSafeRotate(self, direction, rotations, condFuncs):
        raise NotImplementedError
    
    def __blindSafeRotate(self, direction, rotations, condFuncs):
        raise NotImplementedError
    
    def safeRotate(self, direction, rotations, condFuncs):
        raise NotImplementedError   
    
    # ========== composite behaviour ========== 
    def randomStep(self, condFuncs):
        raise NotImplementedError
    
    
    def checkConditions(self, condFuncs):
        self.u.updateSensorVals()
                
        for c in condFuncs:
            if not c():
                return False
        return True
    
    def __init__(self, utils):
        self.u = utils
        
        speed = 60 # the general percentage of maximum speed used as default rotation-speed.
        self.speedPerc = SpeedPercent(speed) 
        self.negSpeedPerc = SpeedPercent(-speed) 
                
        # 1.125 is about the amount of wheel rotations to make a 180 degree turn
        self.one80Rotations = 1.125
        
        self.engine = MoveTank(OUTPUT_A, OUTPUT_D)
        self.left_motor = LargeMotor(OUTPUT_A)