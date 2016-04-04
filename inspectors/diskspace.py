from fnmatch import fnmatch
from inspector import Inspector

class DiskSpace(Inspector):
	def __init__(self, driver, device = None, mount = "/"):
		self._driver = driver
		self._device = device
		self._mount = mount

	def getName(self):
		return "Disk Space"

	def getMetrics(self):
		df = self._driver.sh("df")

		metric = None

		#Parse and find matching metric
		for line in df['stdout'].splitlines():
			segs = line.split()
			if self._device and fnmatch(segs[0], self._device): #mount point
				metric = segs
				break
			if self._mount and fnmatch(segs[5], self._mount):
				metric = segs
				break

		if not metric:
			return {}

		KB_TO_GB = 1024 * 1024
		return {
			"size" : int(metric[1]) / KB_TO_GB,
			"used" : int(metric[2]) / KB_TO_GB,
			"available" : int(metric[3]) / KB_TO_GB,
			"percent_full" : int(metric[4][:-1])
		}

	def getSummary(self):
		return self._driver.sh("df -h")['stdout']