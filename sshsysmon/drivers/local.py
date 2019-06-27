from lib.plugins import Driver
import os
import subprocess

class Local(Driver):
	def __init__(self, path = "/proc"):
		Driver.__init__(self)
		self._path = path

	def readProc(self, path):
		return open(os.path.join(self._path, path), 'r').read()

	def sh(self, cmd):
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		stdout, stderr = proc.communicate()

		return {
			"stdout": stdout.decode('utf-8'),
			"stderr": stderr.decode('utf-8'),
			"status": proc.returncode
		}

	def getHost(self):
		return "127.0.0.1"

def create(args):
	return Local(**args)