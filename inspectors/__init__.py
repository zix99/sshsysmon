from meminfo import MemInfo
from diskspace import DiskSpace
from loadavg import LoadAvg
from process import Process
from tcp import Tcp
from executer import Exec

def createInspector(name, driver, config):
	if name == "memory":
		return MemInfo(driver, **config)
	if name == "disk":
		return DiskSpace(driver, **config)
	if name == "loadavg":
		return LoadAvg(driver, **config)
	if name == "process":
		return Process(driver, **config)
	if name == "tcp":
		return Tcp(driver, **config)
	if name == "exec":
		return Exec(driver, **config)
	
	raise Exception("Unknown inspector type %s" % name)