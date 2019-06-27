from lib.plugins import Inspector
from io import StringIO
from lib.util import ByteSize, parsers

"""
Description:
	Inspects the memory of the remote host
Metrics:
	- mem_total:	ByteSize of the total memory on the host
	- mem_free:		The memory free on the host
	- cached:		The amount of memory that the kernel is using for caching
	- swap_total:	The total amount of swap available
	- swap_free:	The total amount of swap free
"""
class MemInfo(Inspector):
	def __init__(self, driver):
		self._driver = driver

	def getMetrics(self):
		vals = parsers.splitLines(self._driver.readProc("meminfo"))
		return {
			"mem_total": ByteSize(vals.get("memtotal"), "kb"),
			"mem_free" : ByteSize(vals.get("memfree"), "kb"),
			"cached" : ByteSize(vals.get("cached"), "kb"),
			"swap_total" : ByteSize(vals.get("swaptotal"), "kb"),
			"swap_free" : ByteSize(vals.get("SwapFree"), "kb")
		}

	def getName(self):
		return "Memory"

	def getSummary(self):
		metrics = self.getMetricsCached()

		o = StringIO()
		o.write(u"Mem Total:  %s\n" % metrics["mem_total"])
		o.write(u"Mem Free :  %s\n" % metrics["mem_free"])
		o.write(u"Swap Total: %s\n" % metrics["swap_total"])
		o.write(u"Swap Free:  %s\n" % metrics["swap_free"])

		return o.getvalue()

def create(driver, args):
	return MemInfo(driver, **args)