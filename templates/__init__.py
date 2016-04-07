from os import path
import json
import logging
import pybars
from util import sanitize

TEMPLATE_PATH = path.dirname(path.realpath(__file__))


# Controlling methods for template building
def __ifEq(this, options, left, right):
	if left == right:
		return options['fn'](this)
	else:
		return options['inverse'](this)

def __replace(this, val, match, withVal):
	return val.replace(match.decode('string_escape'), withVal.decode('string_escape'))

def __coalesce(this, *args):
	for arg in args:
		if arg: return arg
	return None

def __alphanum(this, val, replaceWith='_'):
	return sanitize(val, replaceWith)

__helpers = {
	'ifEq' : __ifEq,
	'replace' : __replace,
	'coalesce' : __coalesce,
	'alphanum': __alphanum
}

def __template(src, data):
	hbCompiler = pybars.Compiler()
	hbTemplate = hbCompiler.compile(unicode(src))
	return hbTemplate(data, helpers = __helpers)

def __getPath(name):
	if name.startswith(".") or name.startswith("/"):
		return name
	return path.join(TEMPLATE_PATH, name + ".hb")

def template(name, data):
	if name:
		tplPath = __getPath(name)
		if path.isfile(tplPath):
			logging.debug("Building template with: " + tplPath)
			return __template(open(tplPath, 'r').read(), data)
		else:
			logging.error("Unable to find requested template: " + name)

	return json.dumps(data)