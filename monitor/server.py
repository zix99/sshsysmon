from channelgroup import *
from alert import *
from util import sanitize
import drivers
import inspectors
import logging

class Server:
	def __init__(self, name, config):
		self._name = name
		self._driver = drivers.createDriver(config.get("driver"), config.get("config", {}))
		self._alerts = config.get("alerts", [])
		self._summary = config.get("summary") or config.get("alerts") or []
		self._channels = config.get("channels", [])


	def createAlerts(self):
		alerts = []

		for alert in self._alerts:
			alert_type = alert.get('type')
			alert_alarms = alert.get('alarms', {})
			alert_config = alert.get('config', {})

			logging.debug("Creating inspector: %s..." % alert_type)

			try:
				inspector = inspectors.createInspector(alert_type, self._driver, alert_config)
				if not inspector:
					raise Exception("Unknown inspector type: %s" % alert_type)

				metrics = inspector.getMetrics()
				if not metrics:
					raise Exception("Inspector returned no data: %s" % inspector.getName())

				for alarm_name, statement in alert_alarms.iteritems():
					alerts.append(Alert(self._name, alarm_name, statement, metrics))

			except Exception,e:
				logging.warning("Error executing inspector %s: %s" % (alert_type, e))
				alerts.append(Alert(self._name, "NO_DATA", "True", {}))

		return alerts

	def getFailedAlerts(self):
		failedAlerts = []
		for alert in self.createAlerts():
			logging.debug("Evaluating alert " + alert.name)
			if alert.eval():
				logging.debug("  ALERT FIRED")
				failedAlerts.append(alert)
		return failedAlerts

	#Notify all channels of any alerts that have been fired
	def notifyChannelsOfAlerts(self):
		channels = ChannelGroup(self._channels)

		alerts = self.getFailedAlerts()
		for alert in alerts:
			logging.debug("Notifying channel of alert: %s" % alert)
			channels.notify(alert)

		return alerts

	# Prints out summary to stdout
	def getSummary(self):
		results = []
		for summary in self._summary:
			summary_type = summary.get('type')
			summary_config = summary.get('config', {})
			summary_alarms = summary.get('alarms', {})

			logging.debug('Creating summary for %s...' % summary_type)
			try:
				logging.debug("Creating inspector...")
				inspector = inspectors.createInspector(summary_type, self._driver, summary_config)
				
				logging.debug("Retrieving metrics...")
				metrics = inspector.getMetrics()

				logging.debug("Processing alarms...")
				alarms = []
				for alarm_name, statement in summary_alarms.iteritems():
					alert = Alert(self._name, alarm_name, statement, metrics)
					alarms.append({
						"name" : alarm_name,
						"fired" : alert.eval(),
						"statement" : statement
						})


				logging.debug("Generating summary metrics...")
				results.append({
					"type" : summary_type,
					"config" : summary_config,
					"text" : inspector.getSummary(),
					"name" : inspector.getName(),
					"metrics" : metrics,
					"alarms" : alarms
				})

			except Exception, e:
				logging.warning("Error executing inspector %s: %s" % (summary_type, e))

		return {
			"name" : self._name,
			"inspectors" : results
		}


