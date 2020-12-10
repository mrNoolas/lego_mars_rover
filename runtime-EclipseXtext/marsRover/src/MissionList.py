#movementslist.py
class MissionList:
	def getMissionSet(self):
		return {
			"testBorderAlign": 
				[
				{
					"moves": 
						[
							self.f.rightRotate(120, "degrees"),
							self.f.forward(5, "rotations"),
						],
					"conditions": 
						[
							self.f.colorCondition({"left", "right", "center"}, {6,})
						]
				},
				{
					"moves": 
						[
							self.f.alignBorder()
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
							self.f.safeForward(4, "rotations"),
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
