from email import Email
from command import Command
from stdout import StdOut

def createChannel(name, args):
	if name == "email":
		return Email(**args)
	if name == "command":
		return Command(**args)
	if name == "stdout":
		return StdOut(**args)
	
	raise Exception("Unknown channel type %s" % name)
