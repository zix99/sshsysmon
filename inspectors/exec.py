import logging
from inspector import Inspector


class Exec(Inspector):
	def __init__(self, driver, command):
		self._driver = driver
		self._cmd = command

	def getMetrics(self):
		return self._driver.sh(self._cmd)

def create(driver, args):
	return Exec(driver, **args)
