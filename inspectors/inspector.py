

class Inspector:
	def __init__(self):
		pass

	def getMetrics(self):
		return {}

	def getName(self):
		return self.__class__.__name__ or "Undefined"