#movementslist.py
class MissionList:
	def getMissionSet(self):
		return {
			"probeAllBorders": 
				[
				{
					"moves": 
						[
							self.f.rightSafeRotate(90, "degrees"),
							self.f.leftSafeRotate(90, "degrees")
						],
					"conditions": 
						[
						]
				},
				],
		}
		
	def __init__(self, dslFunctions):
		self.f = dslFunctions
