#movementslist.py
class MissionList:
	def getMissionSet(self):
		return {
			"test": 
				[
				{
					"moves": 
						[
							self.f.randomStep(),
						],
					"conditions": 
						[
							self.f.colorCondition({}),
							self.f.colorCondition({2}),
						]
				},
				],
		}
		
	def __init__(self, dslFunctions):
		self.f = dslFunctions
