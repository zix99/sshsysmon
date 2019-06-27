from lib.plugins import Inspector
from io import StringIO
from fnmatch import fnmatch
from lib.util import ByteSize, parsers

"""
Description:
	Gets network interface traffic statistics
Constructor:
	- match: Wildcard match for interface name (Default: None)
	- hideEmpty: Hide interfaces
Metrics:

"""
class Network(Inspector):
	def __init__(self, driver, match = None, hideEmpty = False):
		self._driver = driver
		self._match = match
		self._hideEmpty = hideEmpty

	def getMetrics(self):
		devices = parsers.splitLines(self._driver.readProc("net/dev"))

		interfaces = {}

		for d,v in devices:
			if (self._match == None or fnmatch(d, self._match)) and (not self._hideEmpty or int(v[1]) > 0 or int(v[9]) > 0):
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
				'received' : ByteSize(sum(map(lambda x: int(x['receive']['bytes']), interfaces.values() ))),
				'transmitted' : ByteSize(sum(map(lambda x: int(x['transmit']['bytes']), interfaces.values() )))
			}
		}

	def getSummary(self):
		data = self.getMetricsCached()
		o = StringIO()

		o.write(u"Totals:\n")
		o.write(u"  Received:    %s\n" % data['totals']['received'])
		o.write(u"  Transmitted: %s\n" % data['totals']['transmitted'])

		for d,metrics in data['interfaces'].items():
			o.write(u"%s\n" % d)

			o.write(u"  Receive:\n")
			o.write(u"    Bytes:   %s\n" % metrics['receive']['bytes'])
			o.write(u"    Packets: %s\n" % metrics['receive']['packets'])
			o.write(u"    Errors:  %s\n" % metrics['receive']['errors'])
			o.write(u"    Drop:    %s\n" % metrics['receive']['drop'])

			o.write(u"  Transmit:\n")
			o.write(u"    Bytes:   %s\n" % metrics['transmit']['bytes'])
			o.write(u"    Packets: %s\n" % metrics['transmit']['packets'])
			o.write(u"    Errors:  %s\n" % metrics['transmit']['errors'])
			o.write(u"    Drop:    %s\n" % metrics['transmit']['drop'])

		return o.getvalue()

	def getName(self):
		return "Network"

def create(driver, args):
	return Network(driver, **args)
