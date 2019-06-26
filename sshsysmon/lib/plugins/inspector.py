from io import StringIO

class Inspector:
	def __init__(self):
		pass

	def getMetrics(self):
		return {}

	def getMetricsCached(self):
		if not hasattr(self, '_metricsCache'):
			self._metricsCache = self.getMetrics()
		return self._metricsCache

	def getName(self):
		return self.__class__.__name__ or "Undefined"

	def getSummary(self, itemFilter = None):
		o = StringIO()

		metrics = self.getMetricsCached()

		if metrics:
			for key in itemFilter or metrics:
				o.write(u"%s: %s\n" % (key.upper(), metrics.get(key, "<Missing>")))
		else:
			o.write(u"Unable to retrieve metrics")

		return o.getvalue()