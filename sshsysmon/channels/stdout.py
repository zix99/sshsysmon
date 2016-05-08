from channel import Channel
import time

class StdOut(Channel):
	DEFAULT_FORMAT = "{time}\t{server}\t{inspector}\t{alert}"

	def __init__(self, format=DEFAULT_FORMAT, timeFormat = "ctime"):
		self._format = format
		self._timeFormat = timeFormat

	def notify(self, model):
		stime = None
		if self._timeFormat == "epoch":
			stime = str(time.time())
		else:
			stime = time.ctime()

		data = {
			'time' : stime
		}
		data.update(model)

		print self._format.format(**data)

def create(args):
	return StdOut(**args)