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
							self.f.forward(2.1, "rotations"),
							
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
							self.f.forward(1.0, "rotations"),
							
							self.f.leftRotate(90, "degrees"),
							self.f.forward(4.4, "rotations"),
							
							self.f.rightRotate(90, "degrees"),
							self.f.forward(0.8, "rotations"),
							
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
