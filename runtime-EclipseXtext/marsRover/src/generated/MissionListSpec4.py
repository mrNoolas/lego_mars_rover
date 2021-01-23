#movementslist.py
class MissionList:
	def getMissionSet(self):
		return {
			"probeAllLakes": 
				[
				{
					"moves": 
						[
							self.f.rightRotate(90, "degrees"),
							self.f.forward(0.3, "rotations"),
							
							self.f.probe(),
						],
					"conditions": 
						[
						]
				},
				{
					"moves": 
						[
							self.f.leftRotate(90, "degrees"),
							self.f.forward(2.2, "rotations"),
							
							self.f.rightRotate(90, "degrees"),
							self.f.forward(4.0, "rotations"),
							
							self.f.probe(),
						],
					"conditions": 
						[
						]
				},
				{
					"moves": 
						[
							self.f.leftRotate(90, "degrees"),
							self.f.forward(2.0, "rotations"),
							
							self.f.leftRotate(90, "degrees"),
							self.f.forward(4.0, "rotations"),
							
							self.f.probe(),
						],
					"conditions": 
						[
						]
				},
				],
			"probeAllBorders": 
				[
				{
					"moves": 
						[
							self.f.forward(100.0, "rotations"),
						],
					"conditions": 
						[
							self.f.colorCondition({"left", "right", "center"}, {6,}),
						]
				},
				{
					"moves": 
						[
							self.f.backward(0.2, "rotations"),
							
							self.f.safeForward(0.2, "rotations"),
						],
					"conditions": 
						[
						]
				},
				{
					"moves": 
						[
							self.f.alignBorder(),
							self.f.probe(),
							self.f.backward(0.5, "rotations"),
						],
					"conditions": 
						[
						]
				},
				{
					"moves": 
						[
							self.f.leftRotate(90, "degrees"),
							self.f.forward(100.0, "rotations"),
						],
					"conditions": 
						[
							self.f.colorCondition({"left", "right", "center"}, {6,}),
						]
				},
				{
					"moves": 
						[
							self.f.backward(0.2, "rotations"),
							
							self.f.safeForward(0.2, "rotations"),
						],
					"conditions": 
						[
						]
				},
				{
					"moves": 
						[
							self.f.alignBorder(),
							self.f.probe(),
							self.f.backward(0.5, "rotations"),
						],
					"conditions": 
						[
						]
				},
				{
					"moves": 
						[
							self.f.leftRotate(90, "degrees"),
							self.f.forward(100.0, "rotations"),
						],
					"conditions": 
						[
							self.f.colorCondition({"left", "right", "center"}, {6,}),
						]
				},
				{
					"moves": 
						[
							self.f.backward(0.2, "rotations"),
							
							self.f.safeForward(0.2, "rotations"),
						],
					"conditions": 
						[
						]
				},
				{
					"moves": 
						[
							self.f.alignBorder(),
							self.f.probe(),
							self.f.backward(0.5, "rotations"),
						],
					"conditions": 
						[
						]
				},
				{
					"moves": 
						[
							self.f.leftRotate(90, "degrees"),
							self.f.forward(100.0, "rotations"),
						],
					"conditions": 
						[
							self.f.colorCondition({"left", "right", "center"}, {6,}),
						]
				},
				{
					"moves": 
						[
							self.f.backward(0.2, "rotations"),
							
							self.f.safeForward(0.2, "rotations"),
						],
					"conditions": 
						[
						]
				},
				{
					"moves": 
						[
							self.f.alignBorder(),
							self.f.probe(),
							self.f.backward(0.5, "rotations"),
						],
					"conditions": 
						[
						]
				},
				],
			"findObstacle": 
				[
				{
					"moves": 
						[
							self.f.randomStep(),
						],
					"conditions": 
						[
							self.f.distanceCondition("front", "lt", 50),
						]
				},
				],
		}
		
	def __init__(self, dslFunctions):
		self.f = dslFunctions
