from local import Local
from ssh import Ssh

def createDriver(name, args):
	if name == "local":
		return Local(**args)
	elif name == "ssh":
		return Ssh(**args)
	
	raise Exception("Unknown driver type %s" % name)
