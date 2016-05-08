#!/usr/bin/env python
import sys
import yaml
import time
import logging
import argparse
from templates import template
from lib.monitor import *
from lib.util import merge

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

	sys.stderr.write("There were %d alert(s) triggered\n" % count)

def run_summary(config, templateName=None):
	servers = []
	for server_name, server in config["servers"].iteritems():
		if server.get('summarize', True):
			logging.debug("Checking server: %s..." % server_name)
			try:
				server = Server(server_name, server)
				servers.append(server.getSummary())
			except Exception, e:
				logging.warning("Unable to add server summary for %s: %s" % (server_name, e))

	data = {
		"ctime" : time.ctime(),
		"servers" : servers,
		"meta" : config.get('meta', {})
	}

	print template(templateName, data)



def parseArgs(args):
	p = argparse.ArgumentParser(description = "Run monitoring against servers defined in config")

	p.add_argument('command', help="Command to execute", choices=['check', 'summary'])
	p.add_argument('configs', metavar='cfg', nargs='+', help="YML config file")

	p.add_argument('-v', '--verbose', action='store_true', help="Enable verbose logging")
	p.add_argument('-m', '--merge', help="Update-merge multiple configs from left to right", action='store_true')
	p.add_argument('-f', '--format', help="Specify template format to output summary (markdown)", default="md")

	return p.parse_args(args)

def main(args):
	opts = parseArgs(args)

	logging.basicConfig(level = logging.DEBUG if opts.verbose else logging.INFO)
	logging.getLogger('paramiko').setLevel(logging.WARNING)

	try:
		config = reduce(
			lambda a,b: merge(a,b, overwrite=opts.merge),
			map(
				lambda filename: yaml.load(open(filename, 'r')),
				opts.configs
				)
			)
	except Exception, e:
		logging.error("Error parsing config: " + str(e))
		sys.exit(1)

	if opts.command == "check":
		run_check(config)
	elif opts.command == "summary":
		run_summary(config, opts.format)
	else:
		show_help()
		sys.exit(1)

if __name__=="__main__":
	main(sys.argv[1:])


