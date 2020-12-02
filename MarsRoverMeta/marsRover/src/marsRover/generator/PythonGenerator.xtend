package marsRover.generator

import marsRover.mrDsl.Align
import marsRover.mrDsl.BackwardMove
import marsRover.mrDsl.ButtonPressCondition
import marsRover.mrDsl.ColorCenter
import marsRover.mrDsl.ColorCondition
import marsRover.mrDsl.ColorLeft
import marsRover.mrDsl.ColorMeasurement
import marsRover.mrDsl.ColorRight
import marsRover.mrDsl.Direction
import marsRover.mrDsl.DistanceBack
import marsRover.mrDsl.DistanceCondition
import marsRover.mrDsl.DistanceConditionBackGT
import marsRover.mrDsl.DistanceConditionBackLT
import marsRover.mrDsl.DistanceConditionFrontGT
import marsRover.mrDsl.DistanceConditionFrontLT
import marsRover.mrDsl.DistanceFront
import marsRover.mrDsl.DistanceMeasurement
import marsRover.mrDsl.DistanceOverBorder
import marsRover.mrDsl.DistanceOverPond
import marsRover.mrDsl.ForwardMove
import marsRover.mrDsl.LakeCondition
import marsRover.mrDsl.LeftMove
import marsRover.mrDsl.Measurement
import marsRover.mrDsl.Missions
import marsRover.mrDsl.Move
import marsRover.mrDsl.Movement
import marsRover.mrDsl.ProbeMeasurement
import marsRover.mrDsl.PushBack
import marsRover.mrDsl.PushLeft
import marsRover.mrDsl.PushRight
import marsRover.mrDsl.RandomMove
import marsRover.mrDsl.RightMove
import marsRover.mrDsl.RotateDir
import marsRover.mrDsl.TouchBackCondition
import marsRover.mrDsl.TouchCondition
import marsRover.mrDsl.TouchLeftCondition
import marsRover.mrDsl.TouchLeftRightCondition
import marsRover.mrDsl.TouchRightCondition
import marsRover.mrDsl.Turndir
import marsRover.mrDsl.WaitMove

class PythonGenerator {
	def static toPython(Missions root)'''
		#movementslist.py
		class missionslList
			def getMissionSet(self):
				return 
				{
					«listMissions(root)»
				}
				
			def __init__(self, functions):
				self.f = functions'''
	
	def static listMissions(Missions root)'''
	«FOR mission: root.missions »
	"«mission.name»": 
		[
		«FOR action : mission.action_sequence»
			«action2code(action)»
		«ENDFOR»	
		]
	«ENDFOR»
	'''
	
	def static dispatch action2code(Movement movement)'''
	{
		"actions":
		[
			«FOR move : movement.movement»
				«checkMove(move)»
			«ENDFOR»
		]
		"conditions":
		[
			«IF movement.condition !== null»«condition2code(movement.condition)»«ENDIF»
			«FOR condition : movement.otherConditions»
				«condition2code(condition)»
			«ENDFOR»
		]
	}'''
	
	def static checkMove(Move move)'''		
		«IF move.dir !== null» «move2code(move.dir)» «ENDIF»
		«IF move.turnDir !== null»«move2code(move.turnDir)» «ENDIF»
		«IF move.rotateDir !== null»«move2code(move.rotateDir)»«ENDIF»'''
	
	
	def static dispatch move2code(Direction dir)'''
		«direction2code(dir)»'''
	
	def static dispatch move2code(Turndir dir)'''
		«IF dir == 'left'»self.f.turnLeft, {},«ENDIF»
		«IF dir == 'right'»self.f.tunRight, {},«ENDIF»'''
	
	def static dispatch move2code(RotateDir dir)'''
		«rotateDir2code(dir)»'''
		
	def static dispatch direction2code(ForwardMove move)'''
		«IF move.distance !== 0»
		self.f.forwardForMove, {"amount": "«move.distance»", "unit : "rotations"},
		«ENDIF»
		«IF move.time !== 0»
		self.f.forwardForMove, {"amount": "«move.time»", "unit" : "seconds"},
		«ENDIF»'''
		
	def static dispatch direction2code(BackwardMove move)'''
		«IF move.distance !== 0»
		self.f.backward, {"amount": "«move.distance»", "unit : "rotations"},
		«ENDIF»
		«IF move.time !== 0»
		self.f.backward, {"amount": "«move.time»", "unit" : "seconds"},
		«ENDIF»'''
		
	def static dispatch direction2code(RandomMove move)'''
		self.f.randomStep, {},'''
		
	def static dispatch direction2code(WaitMove move)'''
		self.f.waitMove, {},'''
		
	def static dispatch rotateDir2code(LeftMove move)'''
		«IF move.degrees !== 0»
		self.f.leftRotate, {"amount": «move.degrees», "unit": "degrees"},
		«ENDIF»
		«IF move.time !== 0»
		self.f.leftRotate, {"amount": «move.time», "unit": "seconds"},
		«ENDIF»'''
		
	def static dispatch rotateDir2code(RightMove move)'''
		«IF move.degrees !== 0»
		self.f.rightRotate, {"amount": «move.degrees», "unit": "degrees"},
		«ENDIF»
		«IF move.time !== 0»
		self.f.rightRotate, {"amount": «move.time» "unit": "seconds"},
		«ENDIF»'''
		
	def static dispatch condition2code(ColorCondition cond)'''
		self.f.colorCondition, {"targetSensors": ["left", "right", "center"], "shouldFind": [«IF cond.color == "black"»1«ENDIF»«IF cond.color == "white"»6«ENDIF»«IF cond.color == "red"»5«ENDIF»«IF cond.color == "yellow"»4«ENDIF»«IF cond.color == "blue"»2«ENDIF»]},'''
	
	def static dispatch condition2code(DistanceCondition cond)'''
		«distanceCondition2code(cond)»'''
	
	def static dispatch distanceCondition2code(DistanceConditionFrontLT cond)'''
		self.f.distanceCondition, {"targetSensor": "front", "operator": "lt", "distance": «cond.distance»},'''
		
	def static dispatch distanceCondition2code(DistanceConditionFrontGT cond)'''
		self.f.distanceCondition, {"targetSensor": "front", "operator": "gt", "distance": «cond.distance»},'''
		
	def static dispatch distanceCondition2code(DistanceConditionBackLT cond)'''
		self.f.distanceCondition, {"targetSensor": "back", "operator": "lt", "distance": «cond.distance»},'''
		
	def static dispatch distanceCondition2code(DistanceConditionBackGT cond)'''
		self.f.distanceCondition, {"targetSensor": "back", "operator": "gt", "distance": «cond.distance»},'''
		
	def static dispatch condition2code(TouchCondition cond)'''
		«touchCondition2code(cond)»'''
	
	def static dispatch touchCondition2code(TouchLeftCondition cond)'''
		«IF cond.isPressed == "buffer is "»
		self.f.touchCondition, {"targetSensors": ["frontLeft"], "value": True},
		«ENDIF»
		«IF cond.isPressed == "buffer is not"»
		self.f.touchCondition, {"targetSensors": ["frontLeft"], "value": False},
		«ENDIF»'''
		
	def static dispatch touchCondition2code(TouchRightCondition cond)''' 
		«IF cond.isPressed == "buffer is "»
		self.f.touchCondition, {"targetSensors": ["frontRight"], "value": True},
		«ENDIF»
		«IF cond.isPressed == "buffer is not"»
		self.f.touchCondition, {"targetSensors": ["frontRight"], "value": False},
		«ENDIF»'''
		
	def static dispatch touchCondition2code(TouchLeftRightCondition cond)''' 
		«IF cond.isPressed == "buffer is "»
		self.f.touchCondition, {"targetSensors": ["frontLeft", "frontRight"], "value": True},
		«ENDIF»
		«IF cond.isPressed == "buffer is not"»
		self.f.touchCondition, {"targetSensors": ["frontLeft", "frontRight"], "value": False},
		«ENDIF»'''
		
	def static dispatch touchCondition2code(TouchBackCondition cond)''' 
		«IF cond.isPressed == "buffer is "»
		self.f.touchCondition, {"targetSensors": ["back"], "value": True},
		«ENDIF»
		«IF cond.isPressed == "buffer is not"»
		self.f.touchCondition, {"targetSensors": ["back"], "value": False},
		«ENDIF»'''
		
	def static dispatch condition2code(LakeCondition cond)'''
		self.f.colorCondition, {"colorToFind": [«IF cond.lake == "red"»5«ENDIF»«IF cond.lake == "yellow"»4«ENDIF»«IF cond.lake == "blue"»2«ENDIF»]},'''
		
	def static dispatch condition2code(ButtonPressCondition cond)'''
		self.f.buttonPressCondition, {},'''
	
	def static dispatch action2code(Measurement m)'''
		«measurement2code(m)»'''
		
	def static dispatch measurement2code(DistanceMeasurement m)'''
		«distanceMeasurement2code(m)»'''
		
	def static dispatch distanceMeasurement2code(DistanceFront m)'''
		self.f.measureDistance, {"targetSensor": "front"},'''

	def static dispatch distanceMeasurement2code(DistanceBack m)'''
		self.f.measureDistance, {"targetSensor": "back"},'''
		
	def static dispatch distanceMeasurement2code(DistanceOverBorder m)'''
		self.f.measureDistanceOverBorder, {},'''

	def static dispatch distanceMeasurement2code(DistanceOverPond m)'''
		self.f.measureDistanceOverPond, {},'''
		
	def static dispatch measurement2code(ColorMeasurement c)'''
		«colorMeasurement2code(c)»'''
		
	def static dispatch colorMeasurement2code(ColorLeft c)'''
		self.f.measureColor, {"targetSensor": "left"},'''

	def static dispatch colorMeasurement2code(ColorRight c)'''
		self.f.measureColor, {"targetSensor": "right"},'''
		
	def static dispatch colorMeasurement2code(ColorCenter c)'''
		self.f.measureColor, {"targetSensor": "center"},'''
		
	def static dispatch pushMeasurement2code(PushLeft p)'''
		self.f.measureTouch, {"targetSensor": "frontLeft"},'''

	def static dispatch pushMeasurement2code(PushRight p)'''
		self.f.measureTouch, {"targetSensor": "frontRight"},'''
		
	def static dispatch pushMeasurement2code(PushBack p)'''
		self.f.measureTouch, {"targetSensor": "back"},'''

	def static dispatch measurement2code(ProbeMeasurement p)'''
		self.f.probe, {},'''
		
	def static dispatch action2code(Align align)'''
		self.f.align, {},'''
}