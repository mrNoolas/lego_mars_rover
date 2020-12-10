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
            self.engine.on_for_rotations(self.negRotSpeedPerc, self.rotSpeedPerc, rotations, block=False)  
        elif direction > 0:
            self.engine.on_for_rotations(self.rotSpeedPerc, self.negRotSpeedPerc, rotations, block=False)
                
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
        self.engine.on_for_rotations(self.genSpeedPerc, self.genSpeedPerc, rotations, block=False)
        
        while not self.checkConditions(condFuncs) and self.engine.is_running :
            continue
        self.engine.off(brake=True)
    
    
    def backward(self, rotations, condFuncs):
        """
        Tries to move backward, but does not guarantee that the robot stays within operational parameters (within the border and away from lakes).
        @param rotations: the number of rotations that each engine must make (both engines run simultaneously)
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        """
        self.engine.on_for_rotations(self.negGenSpeedPerc, self.negGenSpeedPerc, rotations, block=False)
        
        while not self.checkConditions(condFuncs) and self.engine.is_running :
            continue
        self.engine.off(brake=True)

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
    
    def safeForward(self, rotations, condFuncs):
        raise NotImplementedError
    
    # ========== composite behaviour ========== 
    def randomStep(self, condFuncs):
        # random rotation in direction
        rot = random.randint(-6, 6) / 10
        result = self.rotate(rot, abs(rot)) # TODO: use safeRotate
        
        if result == 1:
            # random forward unless collision
            dr = random.randint(5, 20) / 10
            self.forward(dr)
        else:
            self.backward(0.20) # 0.2 seems to be the ideal value here; it performs better than 0.15 and 0.25
    
    
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
        self.genSpeedPerc = SpeedPercent(speed) 
        self.negGenSpeedPerc = SpeedPercent(-speed) 
        
        rotationSpeed = 20
        self.rotSpeedPerc = SpeedPercent(rotationSpeed)
        self.negRotSpeedPerc = SpeedPercent(-rotationSpeed)
                
        # 1.125 is about the amount of wheel rotations to make a 180 degree turn
        self.one80Rotations = 1.125
        
        self.engine = MoveTank(OUTPUT_A, OUTPUT_D)
        self.probeMotor = MediumMotor(OUTPUT_B)
        
        
        