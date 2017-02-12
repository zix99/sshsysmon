from inspector import Inspector

"""
Description:
	Determines the load average of the remote host
Metrics:
	- load_1m: load for the past minute
	- load_5m: load for the past 5 minutes
	- load_15m: load for the past 15 minutes
"""
class LoadAvg(Inspector):
	def __init__(self, driver):
		self._driver = driver

	def getMetrics(self):
		data = self._driver.readProc("loadavg").split()

		return {
			"load_1m" : float(data[0]),
			"load_5m" : float(data[1]),
			"load_15m" : float(data[2])
		}

	def getName(self):
		return "CPU Load Average"

def create(driver, args):
	return LoadAvg(driver, **args)