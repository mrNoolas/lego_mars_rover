# MovementController.py

from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedPercent, MediumMotor
from time import sleep
from ev3dev2.sensor.lego import ColorSensor
import random
import math

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
        @param direction: the direction to look in (-1 left (counterclockwise), 1 right (clockwise)), 0 forward
        @param rotations: the maximum amount of rotations to look for
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        @return: Whether a sensor is on a border or not
        """    
        if direction == 0:
            self.__setSpeedSlow()
            self.forward(self, 10, condFuncs + [lambda: self.u.colorSensorOnBorder(borderColor)])
            self.__setSpeedNormal()
        else:
            self.rotate(direction, rotations, condFuncs + [lambda: self.u.colorSensorOnBorder(borderColor)])
        return self.u.colorSensorOnBorder(borderColor)        
        
    
    def __rotateAroundColorSensorOnBorder(self, side, angle, condFuncs, borderColor):
        """
        Calculates the place where the center of the robot (relative to the wheels) should end up, rotates the robot in that direction and moves there in a straight line.
        @param side: which color sensor to rotate around (left or right).
        @param angle: the angle to rotate relative to the colorsensor in degrees
        """
        radius = 117.4 # radius from sensor to center of robot relative to wheels (see robot config)
        c = 69 # x offset of sensor relative to center line of robot (see robot config)
        beta = 90 - (angle / 2)
        gamma = beta - math.degrees(math.asin(c / radius))
        print(gamma)
        distance = 2 * radius * math.sin(math.radians(angle / 2))
        
        direction = -1
        if side == "left":
            direction = 1
        
        self.__setSpeedSlow()
        
        self.rotate(direction, self.angleToRotations(gamma), condFuncs)
        self.forward(self.distanceToRotations(distance), condFuncs)
        self.rotate(-direction, self.angleToRotations(gamma + 10), condFuncs)
        self.rotate(direction, self.angleToRotations(10), condFuncs + [lambda: self.u.colorSensorOnBorder(borderColor)])
        
        self.__setSpeedTurtle()
        # Pull to the inner edge of the border to prevent errors (but only if not both sensors are on the border)
        if not self.u.lastColorL == COLOR_WHITE and self.u.lastColorR == COLOR_WHITE:
            self.backward(0.3, [lambda: not self.u.colorSensorOnBorder(borderColor)])
            self.forward(0.3, [lambda: self.u.colorSensorOnBorder(borderColor)])
        
        self.__setSpeedNormal()
    
    
    def alignWithBorder(self, condFuncs):
        """
        Attempt to put all three sensors on the white border of the map. The robot must be able to see a border from its current postion. It is recommended to set a color sensor on the border before calling this function.
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        @return: Whether the alignment was successful or not
        """
    
        if not self.u.colorSensorOnBorder(COLOR_WHITE) and not self.__findBorder(-1, self.angleToRotations(400), condFuncs, COLOR_WHITE):
            self.u.mSpeak("Could not find border")
            return False       
        
        '''originalDirection = ""
        if self.u.lastColorL == COLOR_WHITE:
            originalDirection = "left"
        elif self.u.lastColorR == COLOR_WHITE:
            originalDirection = "right"
            
        angle = 5'''
        
        # while not aligned properly yet
        while not (self.u.lastColorL == COLOR_WHITE and self.u.lastColorC == COLOR_WHITE and self.u.lastColorR == COLOR_WHITE):
            direction = ""              
            if self.u.lastColorL == COLOR_WHITE:
                direction = "left"
            elif self.u.lastColorR == COLOR_WHITE:
                direction = "right"
            else:
                # hopefully does not happen
                self.u.reportInvalidState("alignWithBorder(...) in MovementController.py", "Encountered else in 'alignWithBorder(...)'. Rover is likely in invalid state.")
                break
            
            #if direction != originalDirection:
            #    angle = 0.5
                
            self.__rotateAroundColorSensorOnBorder(direction, 5, condFuncs, COLOR_WHITE)
            
            if self.u.lastColorL == COLOR_WHITE and self.u.lastColorR == COLOR_WHITE:
                self.__setSpeedTurtle()
                self.forward(0.3, condFuncs + [lambda: self.u.lastColorL != COLOR_WHITE or self.u.lastColorR != COLOR_WHITE or self.u.lastColorC == COLOR_WHITE])
                if not (self.u.lastColorL == COLOR_WHITE and self.u.lastColorC == COLOR_WHITE and self.u.lastColorR == COLOR_WHITE):
                    self.backward(0.3, condFuncs)
                    self.forward(0.3, condFuncs + [lambda: self.u.colorSensorOnBorder(COLOR_WHITE)])
                self.__setSpeedNormal()
        
        self.__setSpeedTurtle()
        self.backward(0.05, condFuncs)
        self.__setSpeedNormal()
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
        circumference = 175.92918860 # of wheel
        return distance / circumference
    
    def angleToRotations(self, angle):
        # 2.25 is about the amount of wheel rotations to make a 360 degree turn
        three60Rotations = 2.25
        return angle / 360 * three60Rotations 
    
    def __setSpeedNormal(self):
        speed = 30 # the general percentage of maximum speed used as default rotation-speed.
        self.genSpeedPerc = SpeedPercent(speed) 
        self.negGenSpeedPerc = SpeedPercent(-speed) 
        
        rotationSpeed = 20
        self.rotSpeedPerc = SpeedPercent(rotationSpeed)
        self.negRotSpeedPerc = SpeedPercent(-rotationSpeed)
        
    def __setSpeedSlow(self):
        speed = 10 # the general percentage of maximum speed used as default rotation-speed.
        self.genSpeedPerc = SpeedPercent(speed) 
        self.negGenSpeedPerc = SpeedPercent(-speed) 
        
        rotationSpeed = 10
        self.rotSpeedPerc = SpeedPercent(rotationSpeed)
        self.negRotSpeedPerc = SpeedPercent(-rotationSpeed)
        
    def __setSpeedTurtle(self):
        """ slower than slow """
        speed = 5 # the general percentage of maximum speed used as default rotation-speed.
        self.genSpeedPerc = SpeedPercent(speed) 
        self.negGenSpeedPerc = SpeedPercent(-speed) 
        
        rotationSpeed = 5
        self.rotSpeedPerc = SpeedPercent(rotationSpeed)
        self.negRotSpeedPerc = SpeedPercent(-rotationSpeed)
        
    
    def __init__(self, utils):
        self.u = utils
        
        self.__setSpeedNormal(
            )  
        # 1.125 is about the amount of wheel rotations to make a 180 degree turn
        self.one80Rotations = 1.125
        
        self.engine = MoveTank(OUTPUT_A, OUTPUT_D)
        self.probeMotor = MediumMotor(OUTPUT_B)
        
        
        