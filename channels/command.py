import subprocess
from channel import Channel
from util.log import *

class Command(Channel):
	def __init__(self, command):
		self._command = command

	def notify(self, model):
		try:
			parsed = self._command.format(**model)
			subprocess.call(parsed, shell=True)
		except Exception, e:
			printError(e)

