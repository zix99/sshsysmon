from os import path
import sys
import imp
import logging

_ROOT = path.join(path.dirname(path.realpath(__file__)), "../../")

def loadPlugin(package, filename, *args):
	modName = "%s.%s" % (__name__, path.basename(filename))
	
	# Search for full filename
	fullPath = path.join(_ROOT, package, filename)
	if not path.isfile(fullPath):
		fullPath = fullPath + ".py"
	if not path.isfile(fullPath):
		raise Exception("Unable to find module: %s" % fullPath)

	try:
		# Load file
		logging.debug("Loading module '%s' at: %s" % (modName, fullPath))
		module = imp.load_source(__name__, fullPath)

		if not module:
			raise Exception('Error loading module source')
		
		# Create instance using `create`
		logging.debug("Creating instance of module '%s'" % modName)
		inst = module.create(*args)

		# Validate
		if not inst:
			raise Exception("Create did not return a valid instance")
		if len(inst.__class__.__bases__) == 0:
			logging.warning("Class '%s' does not inherit from base class", modName)

		return inst
	except Exception as e:
		logging.error("Error loading module: %s" % e)
		raise Exception("Error loading module: %s" % e)

