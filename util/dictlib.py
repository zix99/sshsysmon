

def merge(a, b, path=[], overwrite=False):
	o = dict(a) # Clone

	for key in b:
		if key in o:
			if isinstance(o[key], dict) and isinstance(b[key], dict):
				o[key] = merge(o[key], b[key], path + [str(key)], overwrite)
			elif o[key] == b[key]:
				pass # Same node
			elif overwrite:
				o[key] = b[key]
			else:
				raise Exception("Conflict at '%s'" % '.'.join(path + [str(key)]))
		else:
			o[key] = b[key]
	return o
