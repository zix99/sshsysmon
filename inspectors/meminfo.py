from inspector import Inspector
from StringIO import StringIO
import parsers

def formatKB(kb):
	units = ["KB", "MB", "GB", "TB"]
	idx = 0
	while kb > 1024 and idx < len(units) - 1:
		kb /= 1024
		idx += 1

	return "%d %s" % (kb, units[idx])

class MemInfo(Inspector):
	def __init__(self, driver):
		self._driver = driver

	def getMetrics(self):
		vals = parsers.splitLines(self._driver.readFile("meminfo"))
		return {
			"mem_total": vals.get("memtotal"),
			"mem_free" : vals.get("memfree"),
			"cached" : vals.get("cached"),
			"swap_total" : vals.get("swaptotal"),
			"swap_free" : vals.get("SwapFree")
		}

	def getName(self):
		return "Memory"

	def getSummary(self):
		metrics = self.getMetrics()

		o = StringIO()
		o.write("## Memory\n")
		o.write("Mem Total:  %s\n" % formatKB(metrics["mem_total"]))
		o.write("Mem Free :  %s\n" % formatKB(metrics["mem_free"]))
		o.write("Swap Total: %s\n" % formatKB(metrics["swap_total"]))
		o.write("Swap Free:  %s\n" % formatKB(metrics["swap_free"]))

		return o.getvalue()