from inspector import Inspector
import parsers

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
