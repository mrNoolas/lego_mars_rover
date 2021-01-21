#movementslist.py
class MissionList:
	def getMissionSet(self):
		return {
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
