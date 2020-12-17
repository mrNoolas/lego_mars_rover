#movementslist.py
class MissionList:
	def getMissionSet(self):
		return {
			"probeAllBorders": 
				[
				{
					"moves": 
						[
							self.f.leftRotate(60, "degrees"),
							self.f.forward(1, "rotations"),
						],
					"conditions": 
						[
							self.f.colorCondition({"left", "right"}, {6})
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
		}
		
	def __init__(self, dslFunctions):
		self.f = dslFunctions
