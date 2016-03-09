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
		self._driver = drivers.createDriver(config.get("driver"), config.get("config", {}))
		self._alerts = config.get("alerts", [])
		self._summary = config.get("summary", [])
		self._channels = config.get("channels", [])


	def get_alerts(self):
		for alert in self._alerts:
			alert_type = alert.get('type')
			alert_alarms = alert.get('alarms', {})
			alert_config = alert.get('config', {})

			printInfo("Checking alert: %s..." % alert_type)

			try:
				inspector = inspectors.createInspector(alert_type, self._driver, alert_config)
				if not inspector:
					raise Exception("Unknown inspector type: %s" % alert_type)

				metrics = inspector.getMetrics()
				if not metrics:
					raise Exception("Inspector returned no data: %s" % inspector.getName())


				for alarm_name, statement in alert_alarms.iteritems():
					try:
						if evalCriteria(statement, metrics):
							yield (True, alert_type, alarm_name)
						else:
							yield (False, alert_type, alarm_name)
					except Exception,e:
						yield (True, alert_type, "EVAL:" + alarm_name)
						printError("Error evaluating alert: %s" % e)

			except Exception,e:
				printError("Error executing inspector %s: %s" % (alert_type, e))
				yield (True, "INSPECTOR_ERROR", str(e))

	def get_fired_alerts(self):
		for fired, alert, name in self.get_alerts():
			if fired:
				yield (alert, name)

	def notify_channels(self, data):
		for channel in self._channels:
			channel_type = channel.get('type')
			channel_config = channel.get('config', {})

			try:
				inst = channels.createChannel(channel_type, channel_config)
				inst.notify(data)
			except Exception, e:
				printError("Error notifying channel: %s" % e)



	def send_alerts(self):
		for alert_type, alert_name in self.get_fired_alerts():
			data = {
				"server" : self._name,
				"metric" : alert_type,
				"alert" : alert_name,
			}
			self.notify_channels(data)
			yield (alert_type, alert_name)

	def printSummary(self):
		for summary in self._summary:
			summary_type = summary.get('type')
			summary_items = summary.get('items', [])
			summary_config = summary.get('config', {})
			try:
				inspector = inspectors.createInspector(summary_type, self._driver, summary_config)
				print "## %s" % inspector.getName()
				metrics = inspector.getMetrics()

				if metrics:
					for key in summary_items:
						print "%s: %s" % (key.upper(), metrics.get(key, "<Missing>"))
				else:
					print "Unable to retrieve metrics"

			except Exception, e:
				printError("Error executing inspector %s: %s" % (summary_type, e))
			print ""


