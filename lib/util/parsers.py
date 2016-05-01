
def splitLines(data, delim = ':'):
	vals = {}

	for line in data.splitlines():
		s = map(lambda x: x.strip(), line.split(delim))
		if len(s) == 2:
			vals[s[0].lower()] = map(lambda x: normalizeDataType(x), s[1].split())

	return Lookup(vals)


def normalizeDataType(val):
	try:
		return int(val)
	except: pass
	try:
		return float(val)
	except: pass
	return val

class Lookup:
	def __init__(self, dic):
		self._data = {}
		for k,v in dic.iteritems():
			self._data[k.upper()] = v if isinstance(v, list) else [v]

	def __getitem__(self, key):
		return self._data[key.upper()]

	def __iter__(self):
		return self._data.iteritems()

	def get(self, key, idx=0, default = None):
		rKey = key.upper()
		if rKey in self._data:
			return self._data[rKey][idx]
		return default
