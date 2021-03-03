# MovementController.py

from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedPercent, MediumMotor
from time import sleep
from ev3dev2.sensor.lego import ColorSensor
import random
import math
from distutils.command.check import check

COLOR_WHITE = ColorSensor.COLOR_WHITE

class MovementController:
    #========== Probe movement ==========
    def probe(self, condFuncs = None):
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
        self.__setSpeedSlow()
        if direction == 0:
            self.forward(self, 10, [lambda: self.u.colorSensorOnBorder(borderColor)])
        else:
            self.rotate(direction, rotations, [lambda: self.u.colorSensorOnBorder(borderColor)])
        self.__setSpeedNormal()
        return self.u.colorSensorOnBorder(borderColor)
    
    def __findBorderWithC(self, direction, rotations = 0):
        """
        Tries to find a border (edge and pond) with the center color sensor by rotating. tries to rotate to the nearest border (which it is not currently on) in the given direction.
        
        @param direction: the direction to look in (-1 left (counterclockwise), 1 right (clockwise)), 0 forward
        @param rotations: the maximum amount of rotations to look for
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        @return: Whether a sensor is on a border or not
        """
        if rotations == 0 :
            rotations = 2 * self.one80Rotations
    
        self.__setSpeedSlow()
        if direction < 0: 
            self.engine.on_for_rotations(self.negRotSpeedPerc, self.rotSpeedPerc, rotations, block=False)  
        elif direction > 0:
            self.engine.on_for_rotations(self.rotSpeedPerc, self.negRotSpeedPerc, rotations, block=False)
            
        onBorder = True
        while self.__canRotateSafely() and self.engine.is_running and (not self.u.lastColorC == COLOR_WHITE or onBorder):
            if not self.u.lastColorC == COLOR_WHITE:
                onBorder = False
                
        self.engine.off(brake=True)
        
        if not self.__canRotateSafely():
            self.u.mSpeak('Border not found!')
            return -1
        elif not self.u.lastColorC == COLOR_WHITE or onBorder: # if onBorder is True, the rotator never left the border it was already on...
            return 0
        return 1        
        
    
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
        self.rotate(direction, self.angleToRotations(10), [lambda: self.u.colorSensorOnBorder(borderColor)])
        
        self.__setSpeedTurtle()
        # Pull to the inner edge of the border to prevent errors (but only if not both sensors are on the border)
        if not self.u.lastColorL == COLOR_WHITE and self.u.lastColorR == COLOR_WHITE:
            self.backward(0.3, [lambda: not self.u.colorSensorOnBorder(borderColor)])
            self.forward(0.3, [lambda: self.u.colorSensorOnBorder(borderColor)])
        
        self.__setSpeedNormal()
    
    
    def alignWithBorder(self, condFuncs):
        """
        Attempt to put all three sensors on the white border of the map. The robot must be able to see a border from its current postion. It is recommended to set a color sensor on the border before calling this function.
        
        # FIXME: Robot does not seem to be able to allign with top and bottom borders????
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        @return: Whether the alignment was successful or not
        """
    
        if not self.u.colorSensorOnBorder(COLOR_WHITE) and not self.__findBorder(-1, self.angleToRotations(400), condFuncs, COLOR_WHITE):
            self.u.mSpeak("Could not find border")
            return False       
        
        originalDirection = ""
        if self.u.lastColorL == COLOR_WHITE:
            originalDirection = "left"
        elif self.u.lastColorR == COLOR_WHITE:
            originalDirection = "right"
            
        angle = 7
        
        
        # while not aligned properly yet
        while not (self.u.lastColorL == COLOR_WHITE and self.u.lastColorC == COLOR_WHITE and self.u.lastColorR == COLOR_WHITE) and not self.checkConditions(condFuncs):
            self.u.updateSensorVals(quick = True)
            
            direction = ""              
            if self.u.lastColorL == COLOR_WHITE:
                direction = "left"
            elif self.u.lastColorR == COLOR_WHITE:
                direction = "right"
            else:
                # hopefully does not happen; try to find border again
                self.u.reportInvalidState("alignWithBorder(...) in MovementController.py", "Encountered else in 'alignWithBorder(...)'. Rover is likely in invalid state.")
                break
            
            # increase the precision of the turn
            if direction != originalDirection:
                angle = 1
                
            if not (self.u.lastColorL == COLOR_WHITE and self.u.lastColorR == COLOR_WHITE):
                self.__rotateAroundColorSensorOnBorder(direction, angle, [lambda: self.u.lastColorL == COLOR_WHITE and self.u.lastColorR == COLOR_WHITE], COLOR_WHITE)
            
            if self.u.lastColorL == COLOR_WHITE and self.u.lastColorR == COLOR_WHITE:
                self.__setSpeedTurtle()
                self.forward(0.3, [lambda: self.u.lastColorL != COLOR_WHITE or self.u.lastColorR != COLOR_WHITE or self.u.lastColorC == COLOR_WHITE])
                if not (self.u.lastColorL == COLOR_WHITE and self.u.lastColorC == COLOR_WHITE and self.u.lastColorR == COLOR_WHITE):
                    self.backward(0.3, condFuncs)
                    self.forward(0.3, [lambda: self.u.colorSensorOnBorder(COLOR_WHITE)])
                self.__setSpeedNormal()
        
        #self.__setSpeedTurtle()
        #self.backward(0.02, condFuncs)
        self.__setSpeedNormal()
        return True
    
    def alignWithPond(self, condFuncs):
        raise NotImplementedError
    
    def __canRotateSafely(self):
        return not (self.u.lastTouchB or self.u.lastDistB > 40 or self.u.lastTouchL or self.u.lastTouchR or self.u.lastDistF < 90)
    
    
    def __blindSafeRotate(self, direction, rotations, condFuncs):
        """
        Returns True if rotation succeeded
        Returns False if rotation failed, but robot is in valid position
        Outputs error and stops robot if it can't recover from an invalid state.
        
        Rotate to find either 0 or 2 crossings within the turning rotations.
        If 0 or 2 borders are found, the rotation is safe, return to desired rotation (The robot may be looking at the border after rotation)
        Else, rotation is unsafe.
        
        This function assumes that the robot starts in a valid state with at least two sensors within the border.
        """
        onBorder = {'left': False, 'right': False, 'center': False} 
        sawOneBorder = {'left': False, 'right': False, 'center': False}
        sawTwoBorders = {'center': False}
        
        self.__setSpeedSlow()
        if direction < 0: 
            self.engine.on_for_rotations(self.negRotSpeedPerc, self.rotSpeedPerc, rotations, block=False)  
        elif direction > 0:
            self.engine.on_for_rotations(self.rotSpeedPerc, self.negRotSpeedPerc, rotations, block=False)
                       
                       
        while not self.checkConditions(condFuncs) and self.engine.is_running and self.__canRotateSafely():
                if self.u.lastColorL != COLOR_WHITE :
                    onBorder["left"] = False
                else :
                    sawOneBorder["left"] = True
                    onBorder["left"] = True
                    
                if self.u.lastColorC != COLOR_WHITE :
                    onBorder["center"] = False
                else :
                    if not sawOneBorder["center"]:
                        sawOneBorder["center"] = True
                    elif not onBorder["center"]:
                        # Currently on border and onBorder has been False, so this is second border occurence
                        sawTwoBorders["center"] = True  
                        
                    onBorder["center"] = True
                    
                if self.u.lastColorR != COLOR_WHITE :
                    onBorder["right"] = False
                else :
                    sawOneBorder["right"] = True                        
                    onBorder["right"] = True
                
        self.engine.off(brake=True)
        
        if not self.__canRotateSafely():
            self.u.mSpeak('Could not rotate, unsafe!')
            if onBorder["center"] or sawTwoBorders["center"]:
                self.__setSpeedNormal()
                return False
            elif sawOneBorder["center"]:
                if self.__findBorderWithC(-direction) == 1:
                    self.__setSpeedNormal()
                    return False
                self.__setSpeedNormal()
                return self.u.reportInvalidState("__blindSafeRotate(...) in MovementController.py", "Rover is outside of field and cannot recover.") # should be unreachable if the environment is static; moving back the way we came should succeed
            else:
                # Try to turn back to the previous border
                if self.__findBorderWithC(-direction) == 1:
                    self.__setSpeedNormal()
                    return False
                self.__setSpeedNormal()
                return self.u.reportInvalidState("__blindSafeRotate(...) in MovementController.py", "Rover is outside of field and cannot recover.")
            
        # Rotations was successful so far. If two borders were seen, then whole turn is successful. (If the robot never left the border, this is also fine)
        if sawTwoBorders["center"] or not sawOneBorder["center"] or onBorder["center"]:
            self.__setSpeedNormal()
            return True
        elif sawOneBorder["center"]:
            # Try to turn back to the previous border
            if self.__findBorderWithC(-direction) == 1:
                self.__setSpeedNormal()
                return False
            self.__setSpeedNormal()
            return self.u.reportInvalidState("__blindSafeRotate(...) in MovementController.py", "Rover is outside of field and cannot recover.")              
        elif self.__findBorderWithC(-direction) == 1: # crossed one border so turn is invalid. Return to previous border
            return False 
        return self.u.reportInvalidState("__blindSafeRotate(...) in MovementController.py", "Encountered final return. Rover is likely in invalid state.")
    
    
    def safeRotate(self, direction, rotations, condFuncs):
        """
        Tries to rotate safely (i.e. keeps robot within borders), but assumes that the robot is in a valid position with at least -one sensor on and one sensor within- or -two sensors on or within- the border) 
        The robot may move backwards slightly to make the rotation safer if only the center color sensor is on the border.
        
        @param direction: the direction to rotate in. 0 = nothing; -1 = left (counterclockwise); 1 = right (clockwise)
        @param rotations: the number of rotations that each engine must make (both engines run simultaneously)
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        
        @return: boolean whether the turn was successful or not
        """
        self.u.updateSensorVals(quick = True)
        if self.u.colorSensorOnBorder(COLOR_WHITE):
            angle = self.rotationsToAngle(rotations)
            self.__setSpeedSlow()
            
            if self.u.lastColorL == COLOR_WHITE and self.u.lastColorR == COLOR_WHITE:
                self.rotate(direction, rotations, condFuncs)
                self.__setSpeedNormal()
                return True
            elif self.u.lastColorL != COLOR_WHITE and self.u.lastColorC == COLOR_WHITE and self.u.lastColorR == COLOR_WHITE:
                if direction != -1 and angle < 210:
                    self.rotate(direction, rotations, condFuncs)
                    self.__setSpeedNormal()
                    return True
                else:
                    self.__setSpeedNormal()
                    return False               
            elif self.u.lastColorL == COLOR_WHITE and self.u.lastColorC == COLOR_WHITE and self.u.lastColorR != COLOR_WHITE:
                if direction != 1 and angle < 210:
                    self.rotate(direction, rotations, condFuncs)
                    self.__setSpeedNormal()
                    return True
                else:
                    self.__setSpeedNormal()
                    return False    
            elif self.u.lastColorL != COLOR_WHITE and self.u.lastColorC == COLOR_WHITE and self.u.lastColorR != COLOR_WHITE:
                self.safeBackward(0.3, [lambda: self.u.lastColorL == COLOR_WHITE or self.u.lastColorR == COLOR_WHITE])
                self.__setSpeedNormal()
                return self.safeRotate(direction, rotations, condFuncs)
            elif self.u.lastColorL != COLOR_WHITE and self.u.lastColorC != COLOR_WHITE and self.u.lastColorR == COLOR_WHITE:
                if direction != 1 and angle < 170:
                    self.rotate(direction, rotations, condFuncs)
                    self.__setSpeedNormal()
                    return True
                else:
                    self.__setSpeedNormal()
                    return False    
            elif self.u.lastColorL == COLOR_WHITE and self.u.lastColorC != COLOR_WHITE and self.u.lastColorR != COLOR_WHITE:
                if direction != -1 and angle < 170:
                    self.rotate(direction, rotations, condFuncs)
                    self.__setSpeedNormal()
                    return True
                else:
                    self.__setSpeedNormal()
                    return False
                
        else:
            return self.__blindSafeRotate(direction, rotations, condFuncs)
    
    def __canMoveForwardSafely(self):
        return not (self.u.colorSensorOnBorder() or self.u.lastTouchL or self.u.lastTouchR or self.u.lastDistF < 70)
    
    def safeForward(self, rotations, condFuncs):
        """
        Tries to move forward and attempts to stay within operational parameters
        @param rotations: the number of rotations that each engine must make (both engines run simultaneously)
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        """
        self.__setSpeedSlow()
        if self.__canMoveForwardSafely():
            self.engine.on_for_rotations(self.genSpeedPerc, self.genSpeedPerc, rotations, brake=True, block=False)    
             
        while self.__canMoveForwardSafely() and self.engine.is_running and not self.checkConditions(condFuncs):
            continue
            
        self.engine.off(brake=True)
        self.__setSpeedNormal()
        if not self.__canMoveForwardSafely():
            print(self.u.lastDistF)
            self.u.mSpeak('Blocked!')
    
    def __canMoveBackwardSafely(self):
        return not (self.u.lastTouchB or self.u.lastDistB > 40)
    
    def safeBackward(self, rotations, condFuncs):
        """
        Tries to move backward and attempts to stay within operational parameters
        @param rotations: the number of rotations that each engine must make (both engines run simultaneously)
        @param condFuncs: the conditionals that must be checked while performing this movement. If the conjunction of all conditionals is True, the movement is stopped ASAP
        """
        self.__setSpeedSlow()
        if self.__canMoveBackwardSafely():
            self.engine.on_for_rotations(self.genSpeedPerc, self.genSpeedPerc, rotations, brake=True, block=False)    
    
        while self.__canMoveBackwardSafely() and self.engine.is_running and not self.checkConditions(condFuncs):
            continue
            
        self.__setSpeedNormal()
        self.engine.off(brake=True)
        if not self.__canMoveForwardSafely():
            self.u.mSpeak('Blocked!')
    
    # ========== composite behaviour ========== 
    def randomStep(self, condFuncs):
        # random rotation in direction
        rot = random.randint(-6, 6) / 10
        result = self.safeRotate(rot, abs(rot), condFuncs) 
        
        if result == 1:
            # random forward unless collision
            dr = random.randint(10, 30) / 10
            self.safeForward(dr, condFuncs)
        else:
            self.safeBackward(0.20, condFuncs) # 0.2 seems to be the ideal value here; it performs better than 0.15 and 0.25
            
    def randomWalk(self, condFuncs):
        while not self.checkConditions(condFuncs):
            self.randomStep(condFuncs)
    
    
    def checkConditions(self, condFuncs):
        """
        Check if the conditions given by condFuncs are met.
        
        @return: disjunction of the results of condFuncs
        """
        self.u.updateSensorVals()
        
        
        cnd = {"df": self.u.lastDistF, "db": self.u.lastDistB}
        
        if len(condFuncs) == 0:
            return False
                
        for c in condFuncs:
            if c(cnd):
                return True
        return False
    
    def distanceToRotations(self, distance):
        circumference = 175.92918860 # of wheel
        return distance / circumference
    
    def angleToRotations(self, angle):
        # 2.25 is about the amount of wheel rotations to make a 360 degree turn
        three60Rotations = 2.25
        return angle / 360 * three60Rotations 
    
    def rotationsToAngle(self, rotations):
        # 2.25 is about the amount of wheel rotations to make a 360 degree turn
        three60Rotations = 2.25
        return rotations / three60Rotations * 360
    
    def __setSpeedNormal(self):
        speed = 20 # the general percentage of maximum speed used as default rotation-speed.
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
        
        
        