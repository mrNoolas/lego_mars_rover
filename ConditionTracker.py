# Conditiontracker.py
import time

class ConditionTracker:
    def tickColors(self):
        """
        Updates the colors that were found. Assumes sensor values in utils are up to date.
        """
        if self.u.lastColorL not in self.__colorsFoundL:
            self.__colorsFoundL.append(self.u.lastColorL)
        if self.u.lastColorR not in self.__colorsFoundR:
            self.__colorsFoundR.append(self.u.lastColorR)
        if self.u.lastColorC not in self.__colorsFoundC:
            self.__colorsFoundC.append(self.u.lastColorC)
    
    def wereColorsFound(self, targets, colors):
        """
        Checks whether the specified colors were found by the sensors in targets.
            @param targets: the sensors that should be checked for occurrences of 'colors'
            @param colors: the colors that must be present
            @return: True if the 'targets' together found all in 'colors'. False otherwise
        """
        colorsFound = []
        if "left" in targets:
            colorsFound.append(self.__colorsFoundL)
        if "right" in targets:
            colorsFound.append(self.__colorsFoundR)
        if "center" in targets:
            colorsFound.append(self.__colorsFoundC)
        
        return colors.issubset(colorsFound)
    
    def startTimer(self):
        self.__startOfTimer = time.time()
    
    def didTimeExpire(self, interval):
        return time.time() - self.__startOfTimer >= interval
    
    def areSensorsTouched(self, sensors, value):
        """
        Checks whether the touch 'sensors' have 'value' as current status
            @param sensors: the sensors to check
            @param value: True or False as desired
            @return: True if all specified sensors have the desired value. False otherwise.
        """ 
        matchingValue = []
        if self.u.lastTouchL == value:
            matchingValue.append("frontLeft")
        if self.u.lastTouchR == value:
            matchingValue.append("frontRight")
        if self.u.lastTouchB == value:
            matchingValue.append("back")
            
        return sensors.issubset(matchingValue)
    
    def reset(self):
        self.__colorsFoundR = []
        self.__colorsFoundL = []
        self.__colorsFoundC = []
        self.__startOfTimer = 0
    
    def __init__(self, utils):
        self.u = utils
        self.reset()