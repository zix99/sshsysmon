from channelgroup import *
from alert import *
from lib.util import sanitize
from lib.plugins import loadPlugin
import logging

class Server:
	def __init__(self, name, config):
		self._name = name
		self._driver = loadPlugin("drivers", config.get("driver"), config.get("config", {}))
		self._monitors = config.get('monitors', []) + config.get('monitors+', [])
		self._channels = config.get('channels', []) + config.get('channels+', [])
		self._meta = config.get('meta', {})


	def createAlerts(self):
		alerts = []

		for monitor in self._monitors:
			monitor_type = monitor.get('type')
			monitor_alarms = monitor.get('alarms', {})
			monitor_config = monitor.get('config', {})

			logging.debug("Creating inspector: %s..." % monitor_type)

			try:
				inspector = loadPlugin("inspectors", monitor_type, self._driver, monitor_config)
				if not inspector:
					raise Exception("Unknown inspector type: %s" % monitor_type)

				metrics = inspector.getMetrics()
				if not metrics:
					raise Exception("Inspector returned no data: %s" % inspector.getName())

				for alarm_name, statement in monitor_alarms.iteritems():
					alerts.append(Alert(self._name, monitor_type, alarm_name, statement, metrics))

			except Exception,e:
				logging.warning("Error executing inspector %s: %s" % (monitor_type, e))
				alerts.append(Alert(self._name, monitor_type, "NO_DATA", "True", {}))

		return alerts

	def getFailedAlerts(self):
		failedAlerts = []
		for alert in self.createAlerts():
			logging.debug("Evaluating alert " + alert.name)
			if alert.eval():
				logging.info("ALERT: %s", alert.name)
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
		for monitor in self._monitors:
			if monitor.get('summarize', True): #Ability to hide at monitor level
				monitor_type = monitor.get('type')
				monitor_config = monitor.get('config', {})
				monitor_alarms = monitor.get('alarms', {})

				logging.debug('Creating summary for %s...' % monitor_type)
				try:
					logging.debug("Creating inspector...")
					inspector = loadPlugin("inspectors", monitor_type, self._driver, monitor_config)
					
					logging.debug("Retrieving metrics...")
					metrics = inspector.getMetrics()

					logging.debug("Processing alarms...")
					alarms = []
					for alarm_name, statement in monitor_alarms.iteritems():
						alert = Alert(self._name, monitor_type, alarm_name, statement, metrics)
						alarms.append({
							"name" : alarm_name,
							"fired" : alert.eval(),
							"statement" : statement
							})


					logging.debug("Generating summary metrics...")
					results.append({
						"type" : monitor_type,
						"config" : monitor_config,
						"text" : inspector.getSummary(),
						"name" : inspector.getName(),
						"metrics" : metrics,
						"alarms" : alarms
					})

				except Exception, e:
					logging.warning("Error executing inspector %s: %s" % (monitor_type, e))

		return {
			"name" : self._name,
			"inspectors" : results,
			"meta" : self._meta
		}


