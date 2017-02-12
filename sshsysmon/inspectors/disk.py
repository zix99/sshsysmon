from fnmatch import fnmatch
from inspector import Inspector
from lib.util import ByteSize

"""
Description:
	DiskSpace executes `df` to discover how much diskspace is remaining

Constructor:
	device: The unix device (eg /dev/sda) to examine for disk space (Default: None)
	mount:	The mount point to examine (Default: /)

Metrics:
	size: ByteSize of the device
	used: ByteSize of used disk space
	available: ByteSize of the available disk space
	percentage_full: The integer percentage of how full the device is
"""
class DiskSpace(Inspector):
	def __init__(self, driver, device = None, mount = "/"):
		self._driver = driver
		self._device = device
		self._mount = mount

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

		return {
			"size" : ByteSize(metric[1], "kb"),
			"used" : ByteSize(metric[2], "kb"),
			"available" : ByteSize(metric[3], "kb"),
			"percent_full" : int(metric[4][:-1])
		}

	def getName(self):
		return "Disk Space: %s" % (self._device or self._mount)

	def getSummary(self):
		metrics = self.getMetrics()
		return "%s: %s total, %s used, %s free (%s%%)\n" % (self._device or self._mount, metrics['size'], metrics['used'], metrics['available'], metrics['percent_full'])

def create(driver, args):
	return DiskSpace(driver, **args)