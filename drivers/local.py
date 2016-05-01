from driver import *
import os
import subprocess
from StringIO import StringIO

class Local(Driver):
	def __init__(self, path = "/proc"):
		Driver.__init__(self)
		self._path = path

	def readFile(self, path):
		return open(os.path.join(self._path, path), 'r').read()

	def sh(self, cmd):
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		proc.wait()
		return {
			"stdout": proc.stdout.read(),
			"stderr": proc.stderr.read(),
			"status": proc.returncode
		}

	def getHost(self):
		return "127.0.0.1"

def create(args):
	return Local(**args)