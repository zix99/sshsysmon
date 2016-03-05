from meminfo import MemInfo
from diskspace import DiskSpace
from loadavg import LoadAvg

def createInspector(name, driver):
	if name == "memory":
		return MemInfo(driver)
	if name == "disk":
		return DiskSpace(driver)
	if name == "loadavg":
		return LoadAvg(driver)
	return None