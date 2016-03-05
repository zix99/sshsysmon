#!/usr/bin/env python
import sys
import yaml
from monitor import *
from util.log import *

def run_check(config):
	count = 0

	for server_name in config["servers"]:
		printInfo("Checking server: %s..." % server_name)

		server = config["servers"][server_name]
		monitor = Monitor(server_name, server)

		for alert in monitor.send_alerts():
			count += 1
			print "ALERT: " + alert[0]

	print "There were %d alert(s) triggered" % count

def run_summary(config):
	for server_name, server in config["servers"].iteritems():
		print "# %s" % server_name
		monitor = Monitor(server_name, server)
		try:
			monitor.printSummary()
		except Exception, e:
			print "ERROR: %s" % e

def show_help():
	print "Usage: sshmon.py <command> <config>"
	print ""
	print "Run monitoring against servers defined in config"
	print ""
	print "Commands:"
	print " check          Check and alerts servers"
	print " summary        Summarize status of servers"

def main(args):
	if len(args) != 2:
		show_help()
		sys.exit(1)

	try:
		config = yaml.load(open(args[1]))
	except Exception, e:
		print "Error parsing config:", str(e)
		sys.exit(1)

	if args[0] == "check":
		run_check(config)
	elif args[0] == "summary":
		run_summary(config)
	else:
		show_help()
		sys.exit(1)

if __name__=="__main__":
	main(sys.argv[1:])


