#!/usr/bin/env python
import sys
import yaml
import time
from monitor import *
import logging
import argparse

def run_check(config):
	count = 0

	for server_name in config["servers"]:
		logging.info("Checking server: %s..." % server_name)

		try:
			server = config["servers"][server_name]
			server = Server(server_name, server)
			count += len(server.notifyChannelsOfAlerts())
		except Exception, e:
			logging.error("Error checking server %s: %s" % (server_name, e))

	print "There were %d alert(s) triggered" % count

def run_summary(config):
	print "System Summary"
	print time.ctime()
	print ""

	for server_name, server in config["servers"].iteritems():
		print "########## %s ##########" % server_name
		try:
			server = Server(server_name, server)
			server.printSummary()
		except Exception, e:
			print "ERROR %s: %s" % (server_name, e)
		print ""

def parseArgs(args):
	p = argparse.ArgumentParser(description = "Run monitoring against servers defined in config")

	p.add_argument('command', help="Command to execute", choices=['check', 'summary'])
	p.add_argument('config', help="YML config file")

	p.add_argument('-v', '--verbose', action='store_true', help="Enable verbose logging")

	return p.parse_args(args)

def main(args):
	opts = parseArgs(args)

	logging.basicConfig(level = logging.DEBUG if opts.verbose else logging.INFO)
	logging.getLogger('paramiko').setLevel(logging.WARNING)

	try:
		config = yaml.load(open(opts.config))
	except Exception, e:
		logging.error("Error parsing config:" + str(e))
		sys.exit(1)

	if opts.command == "check":
		run_check(config)
	elif opts.command == "summary":
		run_summary(config)
	else:
		show_help()
		sys.exit(1)

if __name__=="__main__":
	main(sys.argv[1:])


