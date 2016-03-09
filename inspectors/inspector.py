from StringIO import StringIO

class Inspector:
	def __init__(self):
		pass

	def getMetrics(self):
		return {}

	def getName(self):
		return self.__class__.__name__ or "Undefined"

	def getSummary(self, itemFilter = None):
		o = StringIO()

		o.write("## %s\n" % self.getName())
		metrics = self.getMetrics()

		if metrics:
			for key in itemFilter or metrics:
				o.write("%s: %s\n" % (key.upper(), metrics.get(key, "<Missing>")))
		else:
			o.write("Unable to retrieve metrics")

		return o.getvalue()