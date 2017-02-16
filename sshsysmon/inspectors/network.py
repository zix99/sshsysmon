from inspector import Inspector
from StringIO import StringIO
from fnmatch import fnmatch
from lib.util import ByteSize, parsers

"""
Description:
	Gets network interface traffic statistics
Constructor:
	- match: Wildcard match for interface name (Default: None)
Metrics:

"""
class Network(Inspector):
	def __init__(self, driver, match = None):
		self._driver = driver
		self._match = match

	def getMetrics(self):
		devices = parsers.splitLines(self._driver.readProc("net/dev"))

		interfaces = {}

		for d,v in devices:
			if self._match == None or fnmatch(d, self._match):
				#0,8:bytes, packets, errs, drop, fifo, frame, compressed, [multicast]
				interfaces[d] = {
					'receive' : {
						'bytes' : ByteSize(v[0]),
						'packets' : v[1],
						'errors' : v[2],
						'drop' : v[3]
					},
					'transmit' : {
						'bytes' : ByteSize(v[8]),
						'packets' : v[9],
						'errors' : v[10],
						'drop' : v[11]
					}
				}

		return {
			'interfaces' : interfaces,
			'totals' : {
				'received' : ByteSize(sum(map(lambda x: int(x['receive']['bytes']), interfaces.itervalues() ))),
				'transmitted' : ByteSize(sum(map(lambda x: int(x['transmit']['bytes']), interfaces.itervalues() )))
			}
		}

	def getSummary(self):
		data = self.getMetrics()
		o = StringIO()

		o.write("Totals:\n")
		o.write("  Received:    %s\n" % data['totals']['received'])
		o.write("  Transmitted: %s\n" % data['totals']['transmitted'])

		for d,metrics in data['interfaces'].iteritems():
			o.write("%s\n" % d)

			o.write("  Receive:\n")
			o.write("    Bytes:   %s\n" % metrics['receive']['bytes'])
			o.write("    Packets: %s\n" % metrics['receive']['packets'])
			o.write("    Errors:  %s\n" % metrics['receive']['errors'])
			o.write("    Drop:    %s\n" % metrics['receive']['drop'])

			o.write("  Transmit:\n")
			o.write("    Bytes:   %s\n" % metrics['transmit']['bytes'])
			o.write("    Packets: %s\n" % metrics['transmit']['packets'])
			o.write("    Errors:  %s\n" % metrics['transmit']['errors'])
			o.write("    Drop:    %s\n" % metrics['transmit']['drop'])

		return o.getvalue()

	def getName(self):
		return "Network"

def create(driver, args):
	return Network(driver, **args)
