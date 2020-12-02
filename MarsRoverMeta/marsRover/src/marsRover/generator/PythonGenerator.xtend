package marsRover.generator

import marsRover.mrDsl.Actions
import marsRover.mrDsl.Align
import marsRover.mrDsl.AlignBorder
import marsRover.mrDsl.AlignPond
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
import marsRover.mrDsl.FondCondition
import marsRover.mrDsl.ForwardMove
import marsRover.mrDsl.LeftMove
import marsRover.mrDsl.Measurement
import marsRover.mrDsl.Missions
import marsRover.mrDsl.MoveKind
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
		class missionsList:
			def getMissionSet(self):
				return {
				«FOR mission: root.missions »
				"«mission.name»": [
					«FOR actions: mission.sequence»
						«actions2code(actions)»
					«ENDFOR»	
					],
				«ENDFOR»
				}
				
			def __init__(self, functions):
				self.f = functions
		'''
	
	def static actions2code(Actions actions)'''
	{
		"action": [ «FOR movement : actions.actions»«movement2code(movement)»«ENDFOR»],
		"conditions": [«IF actions.condition !== null»«condition2code(actions.condition)»«ENDIF»
			«IF actions.otherConditions !== null»
			«FOR condition : actions.otherConditions»
				«condition2code(condition.cond)»
			«ENDFOR»
			«ENDIF»
		]
	},'''
	
	def static dispatch movement2code(MoveKind mk)'''		
		«IF mk.dir !== null» «move2code(mk.dir)» «ENDIF»
		«IF mk.turnDir !== null»«move2code(mk.turnDir)» «ENDIF»
		«IF mk.rotateDir !== null»«move2code(mk.rotateDir)»«ENDIF»'''
		
	def static dispatch movement2code(Align align)'''
		«align2code(align)»'''
	
	def static dispatch movement2code(Measurement m)'''
		«measurement2code(m)»'''
	
	def static dispatch move2code(Direction dir)'''
		«direction2code(dir)»'''
	
	def static dispatch move2code(Turndir dir)'''
		«IF dir == 'left'»self.f.turnLeft(),«ENDIF»
		«IF dir == 'right'»self.f.turnRight(),«ENDIF»'''
	
	def static dispatch move2code(RotateDir dir)'''
		«rotateDir2code(dir)»'''
		
	def static dispatch direction2code(ForwardMove move)'''
		«IF move.distance !== 0»
		self.f.forwardForMove(«move.distance», "rotations"),
		«ENDIF»
		«IF move.time !== 0»
		self.f.forwardForMove(«move.time», "seconds"),
		«ENDIF»'''
		
	def static dispatch direction2code(BackwardMove move)'''
		«IF move.distance !== 0»
		self.f.backward(«move.distance», "rotations"),
		«ENDIF»
		«IF move.time !== 0»
		self.f.backward(«move.time», "seconds"),
		«ENDIF»'''
		
	def static dispatch direction2code(RandomMove move)'''
		self.f.randomStep(),'''
		
	def static dispatch direction2code(WaitMove move)'''
		self.f.waitMove(),'''
		
	def static dispatch rotateDir2code(LeftMove move)'''
		«IF move.degrees !== 0»
		self.f.leftRotate(«move.degrees», "degrees"),
		«ENDIF»
		«IF move.time !== 0»
		self.f.leftRotate(«move.time», "seconds"),
		«ENDIF»'''
		
	def static dispatch rotateDir2code(RightMove move)'''
		«IF move.degrees !== 0»
		self.f.rightRotate(«move.degrees», "degrees"),
		«ENDIF»
		«IF move.time !== 0»
		self.f.rightRotate(«move.time», "seconds"),
		«ENDIF»'''
		
	def static dispatch condition2code(FondCondition cond)'''
		self.f.colorCondition([«IF cond.fond == "red"»5«ENDIF»«IF cond.fond == "yellow"»4«ENDIF»«IF cond.fond == "blue"»2«ENDIF»]),'''
		
	def static dispatch condition2code(ColorCondition cond)'''
		self.f.colorCondition(["left", "right", "center"], [«IF cond.color == "black"»1«ENDIF»«IF cond.color == "white"»6«ENDIF»«IF cond.color == "red"»5«ENDIF»«IF cond.color == "yellow"»4«ENDIF»«IF cond.color == "blue"»2«ENDIF»]),'''
		
	def static dispatch condition2code(DistanceCondition cond)'''
		«distanceCondition2code(cond)»'''
	
	def static dispatch distanceCondition2code(DistanceConditionFrontLT cond)'''
		self.f.distanceCondition("front", "lt", «cond.distance»),'''
		
	def static dispatch distanceCondition2code(DistanceConditionFrontGT cond)'''
		self.f.distanceCondition("front", "gt", «cond.distance»),'''
		
	def static dispatch distanceCondition2code(DistanceConditionBackLT cond)'''
		self.f.distanceCondition("back", "lt", «cond.distance»),'''
		
	def static dispatch distanceCondition2code(DistanceConditionBackGT cond)'''
		self.f.distanceCondition("back", "gt", «cond.distance»),'''
		
	def static dispatch condition2code(TouchCondition cond)'''
		«touchCondition2code(cond)»'''
	
	def static dispatch touchCondition2code(TouchLeftCondition cond)'''
		«IF cond.isPressed == "buffer is "»
		self.f.touchCondition(["frontLeft"], True),
		«ENDIF»
		«IF cond.isPressed == "buffer is not"»
		self.f.touchCondition(["frontLeft"], False),
		«ENDIF»'''
		
	def static dispatch touchCondition2code(TouchRightCondition cond)''' 
		«IF cond.isPressed == "buffer is "»
		self.f.touchCondition(["frontRight"], True),
		«ENDIF»
		«IF cond.isPressed == "buffer is not"»
		self.f.touchCondition(["frontRight"], False),
		«ENDIF»'''
		
	def static dispatch touchCondition2code(TouchLeftRightCondition cond)''' 
		«IF cond.isPressed == "buffer is "»
		self.f.touchCondition(["frontLeft", "frontRight"], True),
		«ENDIF»
		«IF cond.isPressed == "buffer is not"»
		self.f.touchCondition(["frontLeft", "frontRight"], False),
		«ENDIF»'''
		
	def static dispatch touchCondition2code(TouchBackCondition cond)''' 
		«IF cond.isPressed == "buffer is "»
		self.f.touchCondition(["back"], True),
		«ENDIF»
		«IF cond.isPressed == "buffer is not"»
		self.f.touchCondition(["back"], False},
		«ENDIF»'''

		
	def static dispatch condition2code(ButtonPressCondition cond)'''
		self.f.buttonPressCondition(),'''
			
	def static dispatch measurement2code(DistanceMeasurement m)'''
		«distanceMeasurement2code(m)»'''
		
	def static dispatch distanceMeasurement2code(DistanceFront m)'''
		self.f.measureDistance("front"),'''

	def static dispatch distanceMeasurement2code(DistanceBack m)'''
		self.f.measureDistance("back"),'''
		
	def static dispatch distanceMeasurement2code(DistanceOverBorder m)'''
		self.f.measureDistanceOverBorder(),'''

	def static dispatch distanceMeasurement2code(DistanceOverPond m)'''
		self.f.measureDistanceOverPond(),'''
		
	def static dispatch measurement2code(ColorMeasurement c)'''
		«colorMeasurement2code(c)»'''
		
	def static dispatch colorMeasurement2code(ColorLeft c)'''
		self.f.measureColor("left"),'''

	def static dispatch colorMeasurement2code(ColorRight c)'''
		self.f.measureColor("right"),'''
		
	def static dispatch colorMeasurement2code(ColorCenter c)'''
		self.f.measureColor("center"),'''
		
	def static dispatch pushMeasurement2code(PushLeft p)'''
		self.f.measureTouch("frontLeft"),'''

	def static dispatch pushMeasurement2code(PushRight p)'''
		self.f.measureTouch("frontRight"),'''
		
	def static dispatch pushMeasurement2code(PushBack p)'''
		self.f.measureTouch("back"),'''

	def static dispatch measurement2code(ProbeMeasurement p)'''
		self.f.probe(),'''

	def static dispatch align2code(AlignPond align)'''
		self.f.alignPond(),'''
		
	def static dispatch align2code(AlignBorder align)'''
		self.f.alignBorder(),'''
		
		

	
		
		
}