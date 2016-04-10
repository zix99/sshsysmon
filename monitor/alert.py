import logging

def getLiteral(val):
	try:
		# If it casts to a number, then we're good
		float(val)
		return val
	except: pass
	return "\"\"\"%s\"\"\"" % val #Treat as multiline string

class Alert:
	def __init__(self, serverName, inspectorType, name, statement, data):
		self.serverName = serverName
		self.name = name
		self.statement = statement
		self.inspector = inspectorType
		self._data = data

	def eval(self):
		try:
			for k in self._data.iterkeys():
				exec("%s = self._data['%s']" % (k, k))
			return eval(self.statement)
		except Exception, e:
			logging.warning("Error validating alert %s:%s: %s" % (self.serverName, self.name, e))
		return True

	def __repr__(self):
		return "[%s:%s:%s]" % (self.serverName, self.inspector, self.name)