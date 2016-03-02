from meminfo import MemInfo

def createInspector(name, driver):
	if name == "memory":
		return MemInfo(driver)
	return None