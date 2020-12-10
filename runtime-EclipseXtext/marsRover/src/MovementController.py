# MovementController.py

from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedPercent, MediumMotor
from time import sleep
from ev3dev2.sensor.lego import ColorSensor
import random

COLOR_WHITE = ColorSensor.COLOR_WHITE

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
    def __findBorder(self, direction, rotations, condFuncs, borderColor = None):
        """
        Tries to find a border (edge and pond) with one of the colorsensors by rotating
        @param direction: the direction to look in (-1 left (counterclockwise), 1 right (clockwise))
        @param rotations: the maximum amount of rotations to look for
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        @return: Whether a sensor is on a border or not
        """    
        self.rotate(direction, rotations, condFuncs.add(lambda: self.u.colorSensorOnBorder(borderColor)))
        return self.u.colorSensorOnBorder(borderColor)
    
    def alignWithBorder(self, condFuncs):
        """
        Attempt to put all three sensors on the white border of the map
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        @return: Whether the alignment was successful or not
        """
        raise NotImplementedError
    
        if not self.u.colorSensorOnBorder(COLOR_WHITE) and not self.__findBorder(-1, self.angleToRotations(400), condFuncs, COLOR_WHITE):
            self.u.mSpeak("Could not find border")
            return False
        
        self.genSpeedPerc = SpeedPercent(10)
        self.negGenSpeedPerc = SpeedPercent(-10)
        self.rotSpeedPerc = SpeedPercent(10)
        self.negRotSpeedPerc = SpeedPercent(-10)
        
        # while not aligned properly yet
        while not (self.u.lastColorL == COLOR_WHITE and self.u.lastColorC == COLOR_WHITE and self.u.lastColorR == COLOR_WHITE):
            if self.u.lastColorL != COLOR_WHITE:
                self.rotate(1, 0.05, {lambda: self.u.lastColorL == COLOR_WHITE})
            elif self.u.lastColorR != COLOR_WHITE:
                self.rotate(-1, 0.05, {lambda: self.u.lastColorR == COLOR_WHITE})
            elif self.u.lastColorC != COLOR_WHITE:
                self.forward(0.01, {lambda: self.u.lastColorC == COLOR_WHITE})
            
            self.forward(2, {lambda: self.u.colorSensorOnBorder(COLOR_WHITE)})
        
        self.__resetSpeed()
        return True
    
    def alignWithPond(self, condFuncs):
        raise NotImplementedError
    
    def __onBorderSafeRotate(self, direction, rotations, condFuncs):
        raise NotImplementedError
    
    def __blindSafeRotate(self, direction, rotations, condFuncs):
        raise NotImplementedError
    
    def safeRotate(self, direction, rotations, condFuncs):
        raise NotImplementedError   
    
    def __canMoveForwardSafely(self):
        return not (self.u.colorSensorOnBorder() or self.u.lastTouchL or self.u.lastTouchR or self.u.lastDistF < 280)
    
    def safeForward(self, rotations, condFuncs):
        """
        Tries to move forward and attempts to stay within operational parameters
        @param rotations: the number of rotations that each engine must make (both engines run simultaneously)
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        """
        if self.__canMoveForwardSafely():
            self.engine.on_for_rotations(self.genSpeedPerc, self.genSpeedPerc, rotations, brake=True, block=False)    
             
        while self.__canMoveForwardSafely() and self.engine.is_running :
            continue
            
        self.engine.off(brake=True)
        if not self.canMoveForward():
            self.u.mSpeak('Blocked!')
    
    def __canMoveBackwardSafely(self):
        return not (self.u.lastTouchB or self.u.lastDistB > 50)
    
    def safeBackward(self, rotations, condFuncs):
        """
        Tries to move backward and attempts to stay within operational parameters
        @param rotations: the number of rotations that each engine must make (both engines run simultaneously)
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        """
        if self.__canMoveBackWardSafely():
            self.engine.on_for_rotations(self.genSpeedPerc, self.genSpeedPerc, rotations, brake=True, block=False)    
    
        while self.__canMoveBackWardSafely() and self.engine.is_running :
            continue
            
        self.engine.off(brake=True)
        if not self.canMoveForward():
            self.u.mSpeak('Blocked!')
    
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
    
    def distanceToRotations(self, distance):
        raise NotImplementedError
    
    def angleToRotations(self, angle):
        # 2.25 is about the amount of wheel rotations to make a 360 degree turn
        three60Rotations = 2.25
        return angle / 360 * three60Rotations 
    
    def __resetSpeed(self):
        speed = 40 # the general percentage of maximum speed used as default rotation-speed.
        self.genSpeedPerc = SpeedPercent(speed) 
        self.negGenSpeedPerc = SpeedPercent(-speed) 
        
        rotationSpeed = 20
        self.rotSpeedPerc = SpeedPercent(rotationSpeed)
        self.negRotSpeedPerc = SpeedPercent(-rotationSpeed)
        
    
    def __init__(self, utils):
        self.u = utils
        
        self.__resetSpeed(
            )  
        # 1.125 is about the amount of wheel rotations to make a 180 degree turn
        self.one80Rotations = 1.125
        
        self.engine = MoveTank(OUTPUT_A, OUTPUT_D)
        self.probeMotor = MediumMotor(OUTPUT_B)
        
        
        