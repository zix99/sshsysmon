from inspector import Inspector
from StringIO import StringIO
from lib.util import ByteSize, parsers

class MemInfo(Inspector):
	def __init__(self, driver):
		self._driver = driver

	def getMetrics(self):
		vals = parsers.splitLines(self._driver.readFile("meminfo"))
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
		metrics = self.getMetrics()

		o = StringIO()
		o.write("Mem Total:  %s\n" % metrics["mem_total"])
		o.write("Mem Free :  %s\n" % metrics["mem_free"])
		o.write("Swap Total: %s\n" % metrics["swap_total"])
		o.write("Swap Free:  %s\n" % metrics["swap_free"])

		return o.getvalue()

def create(driver, args):
	return MemInfo(driver, **args)