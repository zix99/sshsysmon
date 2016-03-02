
def normalize_data(val):
	try:
		return int(val)
	except: pass
	try:
		return float(val)
	except: pass
	return val


# Base class for parsing common proc files
class CommonProc:
	def __init__(self, data):
		self._map = {}

		for line in data.splitlines():
			s = map(lambda x: x.strip(), line.split(":"))
			if len(s) == 2:
				self._map[s[0].lower()] = map(lambda x: normalize_data(x), s[1].split())

	def get(self, key, index=0, dflt = None):
		k = key.lower()
		if k in self._map:
			return self._map[k][index]
		return dflt
