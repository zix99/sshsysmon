from inspector import Inspector

class LoadAvg(Inspector):
	def __init__(self, driver):
		self._driver = driver

	def getMetrics(self):
		data = self._driver.readFile("loadavg").split()

		return {
			"load_1m" : float(data[0]),
			"load_5m" : float(data[1]),
			"load_15m" : float(data[2])
		}

	def getName(self):
		return "CPU Load Average"

def create(driver, args):
	return LoadAvg(driver, **args)