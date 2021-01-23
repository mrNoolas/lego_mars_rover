#movementslist.py
class MissionList:
	def getMissionSet(self):
		return {
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
							self.f.safeForward(0.2, "rotations")
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
							self.f.alignBorder(),
							self.f.probe(),
						],
					"conditions": 
						[
						]
				},
				{
					"moves": 
						[
							self.f.backward(3.0, "rotations"),
							
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
							self.f.alignBorder(),
							self.f.probe(),
						],
					"conditions": 
						[
						]
				},
				{
					"moves": 
						[
							self.f.backward(3.0, "rotations"),
							
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
							self.f.alignBorder(),
							self.f.probe(),
						],
					"conditions": 
						[
						]
				},
				],
		}
		
	def __init__(self, dslFunctions):
		self.f = dslFunctions
