# MovementController.py

from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedRPS, SpeedPercent, LargeMotor, MediumMotor
from time import sleep
import random

class MovementController:
    #========== Probe movement ==========
    def probe(self):
        """ Rotates the probe outward and back in a theatrical fashion. """
        self.probeMotor.on_for_rotations(SpeedPercent(-3), 0.2, True, True)
        sleep(0.5)
        self.probeMotor.on_for_rotations(SpeedPercent(10), 0.2, True, True)        
    
    
    # ========== basic movements ==========
    def rotate(self, direction, rotations, condFuncs):
        """
        Tries to rotate, but does not guarantee that all sensors and parts (particularly the color sensors) stay within the border.
        
        @param direction: the direction to rotate in. 0 = nothing; -1 = left (counterclockwise); 1 = right (clockwise)
        @param rotations: the number of rotations that each engine must make (both engines run simultaneously)
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        
        @return: boolean conjunction of condFuncs
        """
        
        if direction < 0: 
            self.engine.on_for_rotations(self.negSpeedPerc, self.speedPerc, rotations, block=False)  
        elif direction > 0:
            self.engine.on_for_rotations(self.speedPerc, self.negSpeedPerc, rotations, block=False)
                
        while not self.checkConditions(condFuncs) and self.engine.is_running :
            continue
        self.engine.off(brake=True)
                
        return self.checkConditions(condFuncs)
    
    
    def forward(self, rotations, condFuncs):
        """
        Tries to move forward, but does not guarantee that the robot stays within operational parameters (within the border and away from lakes).
        @param rotations: the number of rotations that each engine must make (both engines run simultaneously)
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        """
        raise NotImplementedError
    
    
    def backward(self, rotations, condFuncs):
        """
        Tries to move backward, but does not guarantee that the robot stays within operational parameters (within the border and away from lakes).
        @param rotations: the number of rotations that each engine must make (both engines run simultaneously)
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        """
        raise NotImplementedError

    def turn(self, turnCircleDiameter, angle, condFuncs):
        raise NotImplementedError
    
    
    # ========== border aware movements ==========
    def __findBorder(self, direction, rotations, condFuncs):
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
        """
        Check if the conditions given by condFuncs are met.
        
        @return: conjunction of the results of condFuncs
        """
        self.u.updateSensorVals()
        
        if len(condFuncs) == 0:
            return False
                
        for c in condFuncs:
            if not c():
                return False
        return True
    
    def __init__(self, utils):
        self.u = utils
        
        speed = 40 # the general percentage of maximum speed used as default rotation-speed.
        self.speedPerc = SpeedPercent(speed) 
        self.negSpeedPerc = SpeedPercent(-speed) 
                
        # 1.125 is about the amount of wheel rotations to make a 180 degree turn
        self.one80Rotations = 1.125
        
        self.engine = MoveTank(OUTPUT_A, OUTPUT_D)
        self.probeMotor = MediumMotor(OUTPUT_B)
        
        
        