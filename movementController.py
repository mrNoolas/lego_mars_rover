# movementController.py

from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedRPS, SpeedPercent, LargeMotor
from time import sleep
import random

class movementController:
    # ========== basic movements ==========
    def rotate(self, direction, rotations, condFunc):
        raise NotImplementedError
    
    def forward(self, rotations, condFunc):
        raise NotImplementedError
    
    def backward(self, rotations, condFunc):
        raise NotImplementedError
    
    def turn(self, turnCircleDiameter, angle, condFunc):
        raise NotImplementedError
    
    
    # ========== border aware movements ==========
    def __findBorder(self, direction, rotations = 0, condFunc):
        raise NotImplementedError
    
    def alignWithBorder(self, condFunc):
        raise NotImplementedError
    
    def __onBorderSafeRotate(self, direction, rotations, condFunc):
        raise NotImplementedError
    
    def __blindSafeRotate(self, direction, rotations, condFunc):
        raise NotImplementedError
    
    def safeRotate(self, direction, rotations, condFunc):
        raise NotImplementedError   
    
    # ========== composite behaviour ========== 
    def randomStep(self, condFunc):
        raise NotImplementedError
    
    
    def __init__(self, utils):
        self.u = utils
        
        speed = 60 # the general percentage of maximum speed used as default rotation-speed.
        self.speedPerc = SpeedPercent(speed) 
        self.negSpeedPerc = SpeedPercent(-speed) 
                
        # 1.125 is about the amount of wheel rotations to make a 180 degree turn
        self.one80Rotations = 1.125
        
        self.engine = MoveTank(OUTPUT_A, OUTPUT_D)
        self.left_motor = LargeMotor(OUTPUT_A)