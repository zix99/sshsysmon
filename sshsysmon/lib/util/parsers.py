
# Parse pairs of deliminated values into a lookup table
# eg:
# a: 123
# b:    567
def splitLines(data, delim = ':'):
	vals = {}

	for line in data.splitlines():
		s = list(map(lambda x: x.strip(), line.split(delim)))
		if len(s) == 2:
			vals[s[0].lower()] = list(map(lambda x: normalizeDataType(x), s[1].split()))

	return Lookup(vals)

# NTry to turn a data type into a numeric
def normalizeDataType(val):
	try:
		return int(val)
	except: pass
	try:
		return float(val)
	except: pass
	return val

# Lookup table changes a dict into a js-style object with __getitem__ acceosrs
class Lookup:
	def __init__(self, dic):
		self._data = {}
		for k,v in dic.items():
			self._data[k.upper()] = v if isinstance(v, list) else [v]

	def __getitem__(self, key):
		return self._data[key.upper()]

	def __iter__(self):
		return iter(self._data.items())

	def get(self, key, idx=0, default = None):
		rKey = key.upper()
		if rKey in self._data:
			return self._data[rKey][idx]
		return default
