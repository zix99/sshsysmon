from commonproc import *

class MemInfo(CommonProc):
	def __init__(self, driver):
		CommonProc.__init__(self, driver.readfile("meminfo"))
		
		self.mem_total = self.get("MemTotal")
		self.mem_free = self.get("MemFree")
		self.cached = self.get("Cached")
		self.swap_total = self.get("SwapTotal")
		self.swap_free = self.get("SwapFree")

	def __str__(self):
		return "Mem Total: {mtotal}".format(mtotal=self.mem_total)
