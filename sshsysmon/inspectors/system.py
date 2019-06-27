from lib.plugins import Inspector
from lib.util import TimeSpan

"""
Description:
	Gets core system metrics
Metrics:
	uptime - TimeSpan of time the system has been up
	idle - TimeSpan of the amount of CPU time idle (will be multipled by CPU)
"""
class System(Inspector):
	def __init__(self, driver):
		self._driver = driver

	def getMetrics(self):
		uptime = self._driver.readProc('uptime').split()

		return {
			'uptime' : TimeSpan(float(uptime[0])),
			'idle' : TimeSpan(float(uptime[1]))
		}

	def getName(self):
		return "System"


def create(driver, args):
	return System(driver, **args)
