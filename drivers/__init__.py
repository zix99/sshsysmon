from local import Local
from ssh import Ssh

def createDriver(name, args):
	if name == "local":
		return Local(**args)
	elif name == "ssh":
		return Ssh(**args)
	return None
