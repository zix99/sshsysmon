from inspector import Inspector
import re
import urllib2
import json as jsonParser

class Http(Inspector):
	def __init__(self, driver, https=False, path='/', port=None, json=False, match=None):
		self._driver = driver
		self._path = path
		self._port = port or (443 if https else 80)
		self._json = json
		self._match = match
		self._https = https

	def getMetrics(self):
		url = "%s://%s:%d%s" % ("https" if self._https else "http", self._driver.getHost(), self._port, self._path)

		out = {
			"match": None,
			"json": {}
		}
		success = True

		try:
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			content = response.read()

			out = {}

			if self._match:
				out['match'] = matches = re.search(self._match, content) != None
				if not matches:
					success = False

			if self._json:
				out['json'] = jsonParser.loads(content)

		except:
			success = False

		out['success'] = success

		return out