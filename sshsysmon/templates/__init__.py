from os import path
import json
import logging
import pybars
import io
from ..lib.util import sanitize

TEMPLATE_PATH = path.dirname(path.realpath(__file__))


# Controlling methods for template building
def __ifEq(this, options, left, right):
	if left == right:
		return options['fn'](this)
	else:
		return options['inverse'](this)

def __replace(this, val, match, withVal):
	return val.replace(match.decode('string_escape'), withVal.decode('string_escape'))

def __format(this, s, *args):
	return s.format(*args)

def __coalesce(this, *args):
	for arg in args:
		if arg: return arg
	return None

def __alphanum(this, val, replaceWith='_'):
	return sanitize(val, replaceWith)

def __numeric(this, val):
	if hasattr(val, '__float__'):
		return float(val)
	if hasattr(val, '__int__'):
		return int(val)
	return 1 if val else 0

def __deepEach(this, options, obj):
	results = []
	def deepWalk(obj, address):
		if isinstance(obj, list):
			for i in range(len(obj)):
				deepWalk(obj[i], '{}[{}]'.format(address, i))
		elif isinstance(obj, dict):
			for k, v in obj.items():
				deepWalk(v, k if not address else '{}.{}'.format(address, k))
		else:
			kwargs = {
				'key': address,
			}
			scope = pybars.Scope(obj, this, options['root'], **kwargs)
			results.extend(options['fn'](scope))
	deepWalk(obj, '')
	return results

__helpers = {
	'ifEq' : __ifEq,
	'replace' : __replace,
	'coalesce' : __coalesce,
	'alphanum': __alphanum,
	'format': __format,
	'numeric': __numeric,
	'deepEach': __deepEach,
}

def __template(src, data):
	hbCompiler = pybars.Compiler()
	hbTemplate = hbCompiler.compile(src)
	return hbTemplate(data, helpers = __helpers)

def __getPath(name):
	if name.startswith("./") or name.startswith("/"):
		return name
	return path.join(TEMPLATE_PATH, name + ".hb")

class __ComplexEncoder(json.JSONEncoder):
	def default(self, obj): # pylint: disable=E0202
		if hasattr(obj, '__json__'):
			return obj.__json__()
		else:
			return json.JSONEncoder.default(self, obj)

def template(name, data):
	if name and name != 'json':
		tplPath = __getPath(name)
		if path.isfile(tplPath):
			logging.debug("Building template with: " + tplPath)
			return __template(io.open(tplPath, 'r', encoding='utf-8').read(), data)
		else:
			logging.error("Unable to find requested template: " + name)

	return json.dumps(data, cls=__ComplexEncoder)