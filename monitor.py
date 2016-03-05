import drivers
import inspectors
import channels
from util.log import *

def evalCriteria(statement, data):
	for k,v in data.iteritems():
		exec("%s = %s" % (k,v))
	return eval(statement)

class Monitor:
	def __init__(self, name, config):
		self._name = name
		self._driver = drivers.createDriver(config["driver"], config["config"])
		self._alerts = config["alerts"]

		self._channels = []
		for channel_type in config["channels"]:
			channel = config["channels"][channel_type]
			inst = channels.createChannel(channel_type, channel)
			self._channels.append(inst)


	def get_alerts(self):
		for alert_type in self._alerts:
			printInfo("Checking alert: %s..." % alert_type)
			alert = self._alerts[alert_type]

			try:
				inspector = inspectors.createInspector(alert_type, self._driver)
				if not inspector:
					raise Exception("Unknown inspector type: %s" % alert_type)

				metrics = inspector.getMetrics()

				for alert_name in alert:
					statement = alert[alert_name]

					if evalCriteria(statement, metrics):
						yield (alert_type, alert_name)
			except Exception,e:
				yield ("INSPECTOR_ERROR", str(e))

	def send_alerts(self):
		for alert_type, alert_name in self.get_alerts():
			for channel in self._channels:
				channel.notify(self._name, alert_type, alert_name)
				yield (alert_type, alert_name)


