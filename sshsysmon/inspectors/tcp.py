from lib.plugins import Inspector
from io import StringIO
import socket

"""
Description:
	Examines if a tcp port is connectable on the host
Constructor:
	- ports: an int, or array of ints, or CSV ints, that represents ports to be tested
Metrics:
	- all:		bool if all ports were connectable
	- port_{n}:	If a given port was connectable, where {n} is the port
"""
class Tcp(Inspector):
	def __init__(self, driver, ports):
		self._driver = driver

		#Input ports as int, CSV string, or pre-made list
		if isinstance(ports, int):
			self._ports = [ports]
		elif isinstance(ports, str):
			self._ports = map(lambda p: int(p.strip()), ports.split(","))
		elif isinstance(ports, list):
			self._ports = map(lambda p: int(p), ports)
		else:
			raise Exception('Invalid data type for ports')

	def getName(self):
		return "TCP Port %s" % self._ports

	def getMetrics(self):
		ret = {}

		for port in self._ports:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ret['port_%d' % port] = (sock.connect_ex((self._driver.getHost(), port)) == 0)
			sock.close()

		ret['all'] = sum(1 for p in ret.values() if not p) == 0

		return ret

	def getSummary(self):
		metrics = self.getMetricsCached();

		o = StringIO()
		for k,v in metrics.items():
			o.write(u"Port %s: %s\n" % (k, "Open" if v else "Closed"))

		return o.getvalue()

def create(driver, args):
	return Tcp(driver, **args)
