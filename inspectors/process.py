from inspector import Inspector
from fnmatch import fnmatch

class Process(Inspector):
	def __init__(self, driver, process):
		self._driver = driver
		self._process = process

	def getMetrics():
		data = self._driver.sh("ps -A u")

		for line in data.splitlines():
			# User, pid, cpu, mem, vsz, rss, tty, stat, start, time, cmd
			parts = line.split()
			if fnmatch(parts[10], self._process):
				#Found it!
				return {
					"user" : parts[0],
					"pid" : parts[1],
					"cpu" : float(parts[2]),
					"mem" : float(parts[3]),
					"tty" : parts[6]
				}


		return None

	def getName():
		return "Process: %s" % self._process