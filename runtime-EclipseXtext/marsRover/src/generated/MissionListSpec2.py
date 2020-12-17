#movementslist.py
class MissionList:
	def getMissionSet(self):
		return {
			"mmd": 
				[
				{
					"moves": 
						[
							self.f.alignBorder(),
						],
					"conditions": 
						[
						]
				},
				],
		}
		
	def __init__(self, dslFunctions):
		self.f = dslFunctions
