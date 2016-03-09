class Alert:
	def __init__(self, serverName, name, statement, data):
		self.serverName = serverName
		self.name = name
		self.statement = statement
		self._data = data

	def eval(self):
		try:
			for k,v in self._data.iteritems():
				exec("%s = %s" % (k,v))
			return eval(self.statement)
		except Exception, e:
			print "Error validating alert %s:%s: %s" % (self.serverName, self.name, e)
		return True

	def __repr__(self):
		return "[%s:%s]" % (self.serverName, self.name)