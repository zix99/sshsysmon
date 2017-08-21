from channel import Channel
import requests
import logging

class WebHook(Channel):
	def __init__(self, url, method = "POST", headers = {}):
		self._url = url;
		self._method = method
		self._headers = headers

	def notify(self, model):
		try:
			req = requests.request(self._method, self._url, data=model, headers=self._headers)
			if req.status_code / 100 != 2:
				raise Exception('Status code not 2xx')
		except Exception, e:
			logging.error("There was an error calling the webhook %s: %s" % (self._url, e))

def create(args):
	return WebHook(**args)