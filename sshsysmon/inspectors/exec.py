import logging
from inspector import Inspector
from lib.util import findTyped
import json

"""
Description:
	Executs a command remotely and returns the entire result of the command as the metric
Metrics:
	The string of the result
"""
class Exec(Inspector):
	def __init__(self, driver, command, json = False, environment = {}, extract = None):
		self._driver = driver
		self._cmd = command
		self._parseJson = json
		self._environment = environment
		self._extract = extract

	def getName(self):
		return "Exec: %s" % self._cmd

	def getMetrics(self):
		# Serialize environment
		envs = str.join(' ', map(lambda (k,v): str.format('{}="{}"', k, v), self._environment.items()))

		# Log; Intentionally don't log formed command, could have secrets
		logging.debug("Executing command: %s", self._cmd)

		# Execute
		cmd = str.format("{} {}", envs, self._cmd)
		ret = self._driver.sh(cmd)

		if ret['status'] != 0:
			raise Exception('Process returned non-zero exit code')

		# Parse
		if self._parseJson:
			parsed = json.loads(ret['stdout'].strip())

			if self._extract:
				extracted = {}
				for k,v in self._extract.items():
					extracted[k] = findTyped(parsed, v)
				return extracted

			return parsed

		return ret


def create(driver, args):
	return Exec(driver, **args)
