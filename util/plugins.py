from os import path
import imp
import logging

def loadPlugin(package, filename, args):
	modName = "%s.%s" % (package, path.basename(filename))
	
	# Search for full filename
	fullPath = path.join(package, filename)
	if not path.isfile(fullPath):
		fullPath = fullPath + ".py"
	if not path.isfile(fullPath):
		raise Exception("Unable to find module: %s" % fullPath)

	try:
		# Load file
		logging.debug("Loading module '%s' at: %s" % (modName, fullPath))
		module = imp.load_source(modName, fullPath)

		if not module:
			raise Exception('Error loading module source')
		
		# Create instance using `create`
		logging.debug("Creating instance of module '%s'" % modName)
		inst = module.create(args)

		if not inst:
			raise Exception("Create did not return a valid instance")

		return inst
	except Exception as e:
		logging.error("Error loading module: %s" % e)
		raise Exception("Error loading module: %s" % e)

