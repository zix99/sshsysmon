from email import Email
from command import Command

def createChannel(name, args):
	if name == "email":
		return Email(**args)
	if name == "command":
		return Command(**args)
	
	raise Exception("Unknown channel type %s" % name)
