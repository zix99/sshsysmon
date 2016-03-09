import subprocess
from channel import Channel

class Command(Channel):
	def __init__(self, command):
		self._command = command

	def notify(self, model):
		parsed = self._command.format(**model)
		subprocess.call(parsed, shell=True)

