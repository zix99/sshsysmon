import subprocess
from channel import Channel

class Command(Channel):
	def __init__(self, command):
		self._command = command

	def notify(self, server, metric, alert):
		try:
			parsed = self._command.format(server=server, metric=metric, alert=alert)
			subprocess.call(parsed, shell=True)
		except Exception, e:
			print e

