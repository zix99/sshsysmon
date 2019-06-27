from lib.plugins import Inspector
import re
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import json as jsonParser

"""
Description:
	Executes a http get-request, and uses its results as the metrics
Constructor:
	- https:	bool if https or not (default: False)
	- path:		The path to execute on the host
	- port:		The port to do the query on (default: 80 or 443)
	- json:		bool if to try to parse results as JSON (default: False)
	- match:	an optional regex string to match the results against to determine success (default: None)
Metrics:
	- match: 	bool if the result matches the match regex (or None if not provided)
	- json:		the resulting json object (or {} if not parsed as json)
	- status:	the http status that was returned
	- success:	If the request was considered a success or not (returns a 200, as well as matches all criteria)
	- url:		The final URL that was requested
"""
class Http(Inspector):
	def __init__(self, driver, https=False, path='/', port=None, json=False, match=None):
		self._driver = driver
		self._path = path
		self._port = port or (443 if https else 80)
		self._json = json
		self._match = match
		self._https = https


	def getUrl(self):
		return "%s://%s:%d%s" % ("https" if self._https else "http", self._driver.getHost(), self._port, self._path)

	def getMetrics(self):
		url = self.getUrl()

		out = {
			"match": None,
			"json": {},
			"status": 0,
			"success": True,
			"url" : url
		}
		
		try:
			logging.debug("Making request to %s", url)
			response = urlopen(url)
			content = response.read()
			out['status'] = response.getcode()

			if self._match:
				out['match'] = matches = re.search(self._match, content) != None
				if not matches:
					out['success'] = False

			if self._json:
				out['json'] = jsonParser.loads(content)
		except Exception as e:
			out['status'] = getattr(e, 'code', 0)
			out['success'] = False

		return out

	def getName(self):
		return "Http: %s" % self._path

def create(driver, args):
	return Http(driver, **args)