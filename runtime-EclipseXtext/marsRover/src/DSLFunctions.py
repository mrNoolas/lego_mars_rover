# DSLFunctions.py

from time import sleep

class DSLFunctions:

    # ========= movements =========
    def __validateMovArgs(self, amount, unit, direction):
        # input validations
        ex = ""
        if amount <= 0:
            ex += "Invalid amount for " + direction + ": amount should be greater than zero. "
                
        if "rotation" in direction:
            if unit != "rotations" and unit != "degrees":
                ex += "Invalid unit for " + direction + ": unit should be 'rotations', 'seconds' or 'degrees'. "
        elif "forward" in direction or "backward" in direction:
            if unit != "rotations" and unit != "cm":
                ex += "Invalid unit for " + direction + ": unit should be 'rotations', 'seconds' or 'cm'. "            
            
        if ex != "": 
            raise Exception(ex)
    
    # ==== rotations ====    
    def rightRotate(self, amount, unit):
        """
        Rotate right
            @param amount: the angle or rotations (determined by unit)
            @param unit: either 'rotations' or 'degrees'
            @return: lambda condFuncs -> physical movement
        """
        self.__validateMovArgs(amount, unit, "right rotation")
        
        if unit == "rotations":
            return lambda condFuncs: self.m.rotate(1, amount, condFuncs)
        else: # degrees
            return lambda condFuncs: self.m.rotate(1, self.m.angleToRotations(amount), condFuncs)

    def leftRotate(self, amount, unit):
        """
        Rotate left
            @param amount: the angle or rotations (determined by unit)
            @param unit: either 'rotations' or 'degrees'
            @return: lambda condFuncs -> physical movement
        """
        self.__validateMovArgs(amount, unit, "left rotation")
        
        if unit == "rotations":
            return lambda condFuncs: self.m.rotate(-1, amount, condFuncs)
        else: # degrees
            return lambda condFuncs: self.m.rotate(-1, self.m.angleToRotations(amount), condFuncs)

    def rightSafeRotate(self, amount, unit):
        """
        Rotate right, safely with regard to borders
            @param amount: the angle or rotations (determined by unit)
            @param unit: either 'rotations' or 'degrees'
            @return: lambda condFuncs -> physical movement
        """
        self.__validateMovArgs(amount, unit, "right safe rotation")
        
        if unit == "rotations":
            return lambda condFuncs: self.m.safeRotate(1, amount, condFuncs)
        else: # degrees
            return lambda condFuncs: self.m.safeRotate(1, self.m.angleToRotations(amount), condFuncs)

    def leftSafeRotate(self, amount, unit):
        """
        Rotate left, safely with regard to borders
            @param amount: the angle or rotations (determined by unit)
            @param unit: either 'rotations' or 'degrees'
            @return: lambda condFuncs -> physical movement
        """
        self.__validateMovArgs(amount, unit, "left safe rotation")
        
        if unit == "rotations":
            return lambda condFuncs: self.m.safeRotate(-1, amount, condFuncs)
        else: # degrees
            return lambda condFuncs: self.m.safeRotate(-1, self.m.angleToRotations(amount), condFuncs)
    
    # ==== straight ====
    
    def forward(self, amount, unit):
        """
        Move forward
            @param amount: the distance or rotations (determined by unit)
            @param unit: either 'rotations' or 'cm'
            @return: lambda condFuncs -> physical movement
        """
        self.__validateMovArgs(amount, unit, "forward direction")
        
        if unit == "rotations":
            return lambda condFuncs: self.m.forward(amount, condFuncs)
        else: # cm
            return lambda condFuncs: self.m.forward(self.m.distanceToRotations(amount), condFuncs)
    
    def safeForward(self, amount, unit):
        """
        Move forward, while avoiding obstructions and borders
            @param amount: the distance or rotations (determined by unit)
            @param unit: either 'rotations' or 'cm'
            @return: lambda condFuncs -> physical movement
        """
        self.__validateMovArgs(amount, unit, "forward direction")
        
        if unit == "rotations":
            return lambda condFuncs: self.m.safeForward(amount, condFuncs)
        else: # cm
            return lambda condFuncs: self.m.safeForward(self.m.distanceToRotations(amount), condFuncs)
    
    def backward(self, amount, unit):
        """
        Move backward
            @param amount: the distance or rotations (determined by unit)
            @param unit: either 'rotations' or 'cm'
            @return: lambda condFuncs -> physical movement
        """
        self.__validateMovArgs(amount, unit, "backward direction")
        
        if unit == "rotations":
            return lambda condFuncs: self.m.backward(amount, condFuncs)
        else: # cm
            return lambda condFuncs: self.m.backward(self.m.distanceToRotations(amount), condFuncs)
        
    def safeBackward(self, amount, unit):
        """
        Move forward, while avoiding obstructions and borders
            @param amount: the distance or rotations (determined by unit)
            @param unit: either 'rotations' or 'cm'
            @return: lambda condFuncs -> physical movement
        """
        self.__validateMovArgs(amount, unit, "backward direction")
        
        if unit == "rotations":
            return lambda condFuncs: self.m.safeBackward(amount, condFuncs)
        else: # cm
            return lambda condFuncs: self.m.safeBackward(self.m.distanceToRotations(amount), condFuncs)
    
    
    def turnLeft(self, turnCircleDiameter, angle):
        """
        Make a turn with left tendency
            @param turnCircleDiameter: turning circle diameter in cm (0 < D <= 20)
            @param angle: the angle relative to the center of the circle to turn
            @return: lambda condFuncs -> physical movement
        """
        if turnCircleDiameter < 0 or turnCircleDiameter > 20 or angle < 0:
            raise Exception("Invalid turn: the diameter should be > 0 and <= 20; the angle should be > 0.")
        
        raise NotImplementedError
    
    def turnRight(self, turnCircleDiameter, angle):
        """
        Make a turn with right tendency
            @param turnCircleDiameter: turning circle diameter in cm (0 < D <= 20)
            @param angle: the angle relative to the center of the circle to turn
            @return: lambda condFuncs -> physical movement
        """
        if turnCircleDiameter < 0 or turnCircleDiameter > 20 or angle < 0:
            raise Exception("Invalid turn: the diameter should be > 0 and <= 20; the angle should be > 0.")
        
        raise NotImplementedError
    
    def randomStep(self):
        """
        Makes a random rotation and a forward move for random distance
        @return: lambda condFuncs -> physical movement
        """
        return self.m.randomStep
        
    # ==== complex movement ====
    def alignPond(self):
        """
        Attempts to align the robot with a pond. Will raise an exception if the robot sees multiple pond borders (colors) in the initial position, or if no borders are visible.
        
        The robot will perform the following steps:
            1. Determine color of the pond based on the visible colors
            2. (Safely) Turn towards the pond, such that the center sensor sees it.
            3. Make sure that the robot is centered by moving forward slowly and rotating
            4. move back such that all color sensors are on the field (i.e. known state)
            
        @return: lambda condFuncs -> physical movement
        """
        return self.m.alignWithPond
    
    def alignBorder(self):
        """
        Attempts to align the robot with a border. Will raise an exception if no color sensor is on a border.
        @return: lambda condFuncs -> physical movement
        """
        return self.m.alignWithBorder
    
    # ========= conditionals =========
    def colorCondition (self, targetSensors, shouldFind):
        """
        Checks if the specified colors are found
        Assumes that utils has recently updated its sensorValues
            @param targetSensors: which sensors to use to find the colors
            @param shouldFind: list of the colors to find using the targetSensors
            @return: func -> boolean
        """
        if not targetSensors.issubset({"left", "right", "center"}) or not shouldFind.issubset(range(11)):
            raise Exception("Invalid arguments for color condition")
        
        # The strange variable assignment is to control the evaluation time of the wereColorsFound function
        return lambda cnd: self.u.wereColorsFound(targetSensors, shouldFind, cnd)
    
    
        
    def distanceCondition (self, targetSensor, comparator, distance):
        """
        Checks if the given distance for the specified sensor is greater than or smaller than (depending comparator) distance
        Assumes that utils has recently updated its sensorValues
            @param targetSensor: front or back
            @param comparator: lt (less than) or gt (greater than)
            @param distance: in cm (0 < distance <= 10000)
            @return: func -> boolean
        """
        if targetSensor not in {"front", "back"} or comparator not in {"lt", "gt"} or distance < 0 or distance > 5000:
            raise Exception("Invalid arguments for distance condition")
        
        # The strange variable assignment in the lambdas is to control the evaluation time
        if targetSensor == "front":
            if comparator == "lt":
                return lambda cnd: cnd["df"] < distance
            else: # gt
                return lambda cnd: cnd["df"] > distance
        else: # back
            if comparator == "lt":
                return lambda cnd: cnd["db"] < distance
            else: # gt
                return lambda cnd: cnd["db"] > distance
            
    """
    L
    R
    B
    LR
    LB
    RB
    LRB
    """
    def __tcL (self, cnd):
        return self.u.lastTouchL
    
    def __ntcL (self, cnd):
        return not self.u.lastTouchL
    
    def __tcR (self, cnd):
        return self.u.lastTouchR
    
    def __ntcR (self, cnd):
        return not self.u.lastTouchR
    
    def __tcB (self, cnd):
        return self.u.lastTouchB
    
    def __ntcB (self, cnd):
        return not self.u.lastTouchB
    
    def __tcLR (self, cnd):
        return self.u.lastTouchL and self.u.lastTouchR
    
    def __ntcLR (self, cnd):
        return not self.u.lastTouchL and not self.u.lastTouchR
    
    def __tcLB (self, cnd):
        return self.u.lastTouchL and self.u.lastTouchB
    
    def __ntcLB (self, cnd):
        return not self.u.lastTouchL and not self.u.lastTouchB
       
    def __tcRB (self, cnd):
        return self.u.lastTouchL and self.u.lastTouchB
    
    def __ntcRB (self, cnd):
        return not self.u.lastTouchL and not self.u.lastTouchB
    
    def __tcLRB (self, cnd):
        return self.u.lastTouchL and self.u.lastTouchR and self.u.lastTouchB
    
    def __ntcLRB (self, cnd):
        return not self.u.lastTouchL and not self.u.lastTouchR and not self.u.lastTouchB
    
    def touchCondition (self, targetSensors, value):
        """
        checks whether the given sensors are pressed or not (depending on the wanted value)
        Assumes that utils has recently updated its sensorValues
            @param targetSensors: a list containing frontLeft, frontRight or back (or a combination thereof)
            @param value: True or False; the function checks whether the sensors have the same status as 'value'
            @return: func -> boolean
        """
        if not targetSensors.issubset({"frontLeft", "frontRight", "back"}) or value not in {True, False}:
            raise Exception("Invalid arguments for touch condition")
        
        if targetSensors == {"frontLeft"}:
            if value:
                return self.__tcL
            return self.__ntcL
            
        elif targetSensors == {"frontRight"}:
            if value:
                return self.__tcR
            return self.__ntcR
            
        elif targetSensors == {"back"}:
            if value:
                return self.__tcB
            return self.__ntcB
        
        elif targetSensors == {"frontLeft", "frontRight"}:
            if value:
                return self.__tcLR
            return self.__ntcLR
            
        elif targetSensors == {"frontLeft", "back"}:
            if value:
                return self.__tcLB
            return self.__ntcLB
            
        elif targetSensors == {"frontRight", "back"}:
            if value:
                return self.__tcRB
            return self.__ntcRB
            
        elif targetSensors == {"frontLeft", "frontRight", "back"}:
            if value:
                return self.__tcLRB
            return self.__ntcLRB
        
        else:
            return print
    
    def timeCondition(self, time, cnd):
        """
        Checks if the time counter for this movement has expired.
            @param time: in seconds
            @return: func -> boolean
        """
        
        return lambda cnd: self.u.didTimeExpire(time, cnd)
    
    def __btnPressCond(self, cnd):
        return self.u.lastBtns
    
    def buttonPressCondition(self):
        """ 
        Checks whether the button on brick1 is pressed, 
            @return: func -> boolean
        """
        return self.__btnPressCond
    
    # ========= measurements =========
    def __measureColorL(self, condFuncs):
        self.u.mSpeak("Left measures the color " + self.u.int2RetColor(self.u.lastColorL))
    
    def __measureColorR(self, condFuncs):
        self.u.mSpeak("Right measures the color " + self.u.int2RetColor(self.u.lastColorR))
    
    def __measureColorC(self, condFuncs):
        self.u.mSpeak("Center measures the color " + self.u.int2RetColor(self.u.lastColorC))
    
    def measureColor(self, targetSensor, condFuncs = None):
        """ 
        Measures the color for targetSensor
        Assumes that utils has recently updated its sensorValues
            @param targetSensor: either left, right or center
            @return: lambda; condFuncs is ignored. (Added for compatibility with movement execution)
        """
        if targetSensor not in {"left", "right", "center"}:
            raise Exception("Invalid arguments for color measurement")
        
        if targetSensor == "left":
            return self.__measureColorL
        elif targetSensor == "right":
            return self.__measureColorR
        else: # center
            return self.__measureColorC  
        
    def __measureDistanceF(self, condFuncs):
        self.u.mSpeak("Ultrasonic sensor in the Front registers a distance of " + str(self.u.lastDistF) + " centimeter.")
        
    def __measureDistanceB(self, condFuncs):
        self.u.mSpeak("Ultrasonic sensor in the back registers a distance of " + str(self.u.lastDistB) + " centimeter.")
    
    def measureDistance(self, targetSensor, condFuncs = None):
        
        """
        Measures the distance using the given targetSensor
        Assumes that utils has recently updated its sensorValues
            @param targetSensor: either front or back
            @return: lambda; condFuncs is ignored. (Added for compatibility with movement execution)
        """
        if targetSensor not in {"front", "back"}:
            raise Exception("Invalid arguments for distance measurement")
            
        if targetSensor == "front":
            return self.__measureDistanceF
        else:
            return self.__measureDistanceB
      
    
    def __measureTouchL(self, condFuncs):
        self.u.mSpeak("Touch sensor in the front left has value" + str(self.u.lastTouchL))
        
    def __measureTouchR(self, condFuncs):
        self.u.mSpeak("Touch sensor in the front right has value" + str(self.u.lastTouchR))
    
    def __measureTouchC(self, condFuncs):
        self.u.mSpeak("Touch sensor in the back has value" + str(self.u.lastTouchB))
      
    def measureTouch (self, targetSensor, condFuncs = None):
        """
        Measures the targeted touch sensor
        Assumes that utils has recently updated its sensorValues
            @param targetSensor: either frontLeft, frontRight or back
            @return: lambda; condFuncs is ignored. (Added for compatibility with movement execution)
        """
        if targetSensor not in {"frontLeft", "frontRight", "back"}:
            raise Exception("Invalid arguments for touch measurement")
        
        if targetSensor == "frontLeft":
            return self.__measureTouchL
        elif targetSensor == "frontRight":
            return self.__measureTouchR
        else: # back
            return self.__measureTouchC
    
    def probe(self):
        """ 
        Attempts to use the probe on the front.
            @return: lambda; condFuncs is ignored. (Added for compatibility with movement execution)
        """
        return self.m.probe
    
    def __wait(self, seconds, condFuncs):
        if not self.m.checkConditions(condFuncs):
            sleep(seconds)
        
    def wait(self, seconds):
        """ 
        Attempts to wait.
            @return: lambda; condFuncs is ignored. (Added for compatibility with movement execution)
        """
        return lambda condFuncs: self.__wait(seconds, condFuncs)
    
    
    # ========= Conversions =========     
    def negate(self, function):
        return lambda: not function()
    
    def __init__(self, movementController, utils):
        self.m = movementController
        self.u = utils
        
