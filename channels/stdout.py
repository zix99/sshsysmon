from channel import Channel
import time

class StdOut(Channel):
	def __init__(self, timeFormat = "ctime"):
		self._timeFormat = timeFormat

	def notify(self, model):
		stime = None
		if self._timeFormat == "epoch":
			stime = str(time.time())
		else:
			stime = time.ctime()

		print "%s\t%s\t%s\t%s" % (stime, model['server'], model['inspector'], model['alert'])
