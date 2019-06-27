

"""
Wrapper for timedelta class to provide nicer access for alarms
"""
class TimeSpan:
	def __init__(self, seconds):
		self._seconds = seconds

	@staticmethod
	def fromTimeDelta(delta):
		return TimeSpan(delta.total_seconds())

	@property
	def seconds(self):
		return self._seconds

	@property
	def minutes(self):
		return self._seconds / 60.0

	@property
	def hours(self):
		return self._seconds / 60.0 / 60.0

	@property
	def days(self):
		return self._seconds / 60.0 / 60.0 / 24.0

	def __json__(self):
		return self._seconds

	def __int__(self):
		return int(self._seconds)

	def __str__(self):
		if self._seconds < 60:
			return "%i seconds" % (self._seconds)
		elif self._seconds < 60 * 60:
			return "%i minutes" % (self.minutes)
		elif self._seconds < 60 * 60 * 24:
			return "%i hours" % (self.hours)
		else:
			return "%i days" % (self.days)

	def __lt__(self, other): return int(self) < int(other)
	def __le__(self, other): return int(self) <= int(other)
	def __eq__(self, other): return int(self) == int(other)
	def __ne__(self, other): return int(self) != int(other)
	def __gt__(self, other): return int(self) > int(other)
	def __ge__(self, other): return int(self) >= int(other)
	