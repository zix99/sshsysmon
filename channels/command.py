import subprocess
from channel import Channel
from util.log import *

class Command(Channel):
	def __init__(self, command):
		self._command = command

	def notify(self, server, metric, alert):
		try:
			parsed = self._command.format(server=server, metric=metric, alert=alert)
			subprocess.call(parsed, shell=True)
		except Exception, e:
			printError(e)

