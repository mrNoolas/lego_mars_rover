# DSLFunctions.py


class DSLFunctions:

    # ========= movements =========
    def __validateMovArgs(self, amount, unit, direction):
        # input validations
        ex = ""
        if amount <= 0:
            ex += "Invalid amount for " + direction + ": amount should be greater than zero. "
                
        if "rotation" in direction:
            if unit != "rotations" and unit != "degrees":
                ex += "Invalid unit for " + direction + ": unit should be 'rotations' or 'degrees'. "
        elif "forward" in direction or "backward" in direction:
            if unit != "rotations" and unit != "cm":
                ex += "Invalid unit for " + direction + ": unit should be 'rotations' or 'cm'. "            
            
        if ex != "": 
            raise Exception(ex)
    
    # ==== rotations ====    
    def rightRotate(self, amount, unit):
        """
        Rotate right
            @param amount: the angle or rotations (determined by unit)
            @param unit: either 'rotations' or 'degrees'
        """
        self.__validateMovArgs(amount, unit, "right rotation")
        
        raise NotImplementedError

    def leftRotate(self, amount, unit):
        """
        Rotate left
            @param amount: the angle or rotations (determined by unit)
            @param unit: either 'rotations' or 'degrees'
        """
        self.__validateMovArgs(amount, unit, "left rotation")
        
        raise NotImplementedError

    def rightSafeRotate(self, amount, unit):
        """
        Rotate right, safely with regard to borders
            @param amount: the angle or rotations (determined by unit)
            @param unit: either 'rotations' or 'degrees'
        """
        self.__validateMovArgs(amount, unit, "right safe rotation")
        
        raise NotImplementedError

    def leftSafeRotate(self, amount, unit):
        """
        Rotate left, safely with regard to borders
            @param amount: the angle or rotations (determined by unit)
            @param unit: either 'rotations' or 'degrees'
        """
        self.__validateMovArgs(amount, unit, "left safe rotation")
        
        raise NotImplementedError
    
    # ==== straight ====
    
    def forward(self, amount, unit):
        """
        Move backward
            @param amount: the distance or rotations (determined by unit)
            @param unit: either 'rotations' or 'cm'
        """
        self.__validateMovArgs(amount, unit, "forward direction")
        
        raise NotImplementedError
    
    def backward(self, amount, unit):
        """
        Move backward
            @param amount: the distance or rotations (determined by unit)
            @param unit: either 'rotations' or 'cm'
        """
        self.__validateMovArgs(amount, unit, "backward direction")
        
        raise NotImplementedError
    
    def turnLeft(self, turnCircleDiameter, angle):
        """
        Make a turn with left tendency
            @param turnCircleDiameter: turning circle diameter in cm (0 < D <= 20)
            @param angle: the angle relative to the center of the circle to turn
        """
        if turnCircleDiameter < 0 or turnCircleDiameter > 20 or angle < 0:
            raise Exception("Invalid turn: the diameter should be > 0 and <= 20; the angle should be > 0.")
        
        raise NotImplementedError
    
    def turnRight(self, turnCircleDiameter, angle):
        """
        Make a turn with right tendency
            @param turnCircleDiameter: turning circle diameter in cm (0 < D <= 20)
            @param angle: the angle relative to the center of the circle to turn
        """
        if turnCircleDiameter < 0 or turnCircleDiameter > 20 or angle < 0:
            raise Exception("Invalid turn: the diameter should be > 0 and <= 20; the angle should be > 0.")
        
        raise NotImplementedError
    
    def randomStep(self):
        """
        Makes a random rotation and a forward move for random distance
        """
        self.turn
        self.m.randomStep()
    
    # ========= conditionals =========
    def colorCondition (self, targetSensors, shouldFind):
        """
        Checks if the specified colors are found
            @param targetSensors: which sensors to use to find the colors
            @param shouldFind: list of the colors to find using the targetSensors
        """
        if not targetSensors.issubset(["left", "right", "center"]) or not shouldFind.issubset(range(11)):
            raise Exception("Invalid arguments for color condition")
            
        raise NotImplementedError
        
    def distanceCondition (self, targetSensor, comparator, distance):
        """
        Checks if the given distance for the specified sensor is greater than or smaller than (depending comparator) distance
            @param targetSensor: front or back
            @param comparator: lt (less than) or gt (greater than)
            @param distance: in cm (0 < distance <= 10000)
        """
        if targetSensor not in ["front", "back"] or comparator not in ["lt", "gt"] or distance < 0 or distance > 10000:
            raise Exception("Invalid arguments for distance condition")
        
        raise NotImplementedError
        
    def touchCondition (self, targetSensors, value):
        """
        checks whether the given sensors are pressed or not (depending on the wanted value)
            @param targetSensors: a list containing frontLeft, frontRight or back (or a combination thereof)
            @param value: True or False; the function checks whether the sensors have the same status as 'value'
        """
        if not targetSensors.issubset(["frontLeft", "frontRight", "back"]) or value not in [True, False]:
            raise Exception("Invalid arguments for touch condition")
        
        raise NotImplementedError
    
    def buttonPressCondition(self):
        """ Checks whether the button on brick1 is pressed"""
        raise NotImplementedError
    
    # ========= measurements =========
    def measureColor(self, targetSensor):
        """ 
        Measures the color for targetSensor
            @param targetSensor: either left, right or center
        """
        if targetSensor not in ["left", "right", "center"]:
            raise Exception("Invalid arguments for color measurement")
        
        raise NotImplementedError
    
    def measureDistance(self, targetSensor):
        """
        Measures the distance using the given targetSensor
            @param targetSensor: either front or back
        """
        if targetSensor not in ["front", "back"]:
            raise Exception("Invalid arguments for distance measurement")
            
        raise NotImplementedError
    
    def measureDistanceOverBorder(self):
        """
        Measure the distance over the border. This function assumes that at least one of the color sensors is currently over a border, and maneuvres the robot based on that.
        
        The robot will perform the following steps:
            1. align color sensors with borders
            2. rotate such that US sensor is facing border
            3. move backwards until the US sensor reads a distance that is significantly larger than earlier (i.e. it moved off the border/map)
        """
        raise NotImplementedError
    
    def measureDistanceOverPond(self):
        """
        Measure the distance over a pond. This function assumes that at least one of the color sensors is currently over the border of the given pond, and maneuvres the robot based on that.
        
        This method will fail if multiple color sensors detect different colors, which are not the base
        
        The robot will perform the following steps:
            1. align color sensors with borders
            2. rotate such that US sensor is facing pond
            3. move backwards until the US sensor reads a distance that is significantly larger than earlier (i.e. it moved off the border/map)
        """
        raise NotImplementedError
    
    def measureTouch (self, targetSensor):
        """
        Measures the targeted touch sensor
            @param targetSensor: either frontLeft, frontRight or back
        """
        if targetSensor not in ["frontLeft", "frontRight", "back"]:
            raise Exception("Invalid arguments for touch measurement")
        
        raise NotImplementedError
    
    def probe(self):
        """ Attempts to use the probe on the front """
        raise NotImplementedError
    
    def probeOverBorder(self):
        """
        Probe over the border. This function assumes that at least one of the color sensors is currently over a border, and maneuvres the robot based on that.
        
        The robot will perform the following steps:
            1. align color sensors with borders
            2. move forward slightly
            3. probe
        """
        raise NotImplementedError
    
    def probeOverPond(self):
        """
        Probe over a pond. This function assumes that at least one of the color sensors is currently over a colored border, and maneuvres the robot based on that.
        
        This method will fail if multiple color sensors detect different colors, which are not the base
        
        The robot will perform the following steps:
            1. align color sensors with borders
            2. move forward slightly
            3. probe pond
        """
        raise NotImplementedError
    
    # ========= Conversions ========= 
    def __distanceToRotations(self, distance):
        raise NotImplementedError
    
    def __angleToRotations(self, angle):
        raise NotImplementedError
    
    def __init__(self, movement, conditions, utils):
        self.m = movement
        self.c = conditions
        self.u = utils
        
