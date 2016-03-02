from driver import *
import os
import subprocess
from StringIO import StringIO

class Local(Driver):
	def __init__(self, path = "/proc"):
		Driver.__init__(self)
		self._path = path

	def readfile(self, path):
		return open(os.path.join(self._path, path), 'r').read()

	def sh(self, cmd):
		proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
		return proc.stdout.read()