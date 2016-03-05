from meminfo import MemInfo
from diskspace import DiskSpace

def createInspector(name, driver):
	if name == "memory":
		return MemInfo(driver)
	if name == "disk":
		return DiskSpace(driver)
	return None