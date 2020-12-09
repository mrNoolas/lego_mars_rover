# MissionList.py

class MissionList:
	def getMissionSet(self):
		return {
			"probeAllBorders":
				[
				{
					"moves":
						[
							self.f.rightRotate(70, "degrees"),
							#self.f.forward(1, "rotations"),
							self.f.probe,
						],
					"conditions":
						[
						]
				},
				{
					"moves":
						[
							#self.f.forward(1, "rotations"),
						],
					"conditions":
						[
							self.f.colorCondition({"left", "right", "center"}, {6, 1,}),
						]
				},
				{
					"moves":
						[
							#self.f.forward(1, "rotations"),
							#self.f.forward(2, "rotations"),
						],
					"conditions":
						[
							self.f.colorCondition({"left", "right", "center"}, {6,}),
						]
				},
				]
			}
		
	def __init__(self, dslFunctions):
		self.f = dslFunctions