from driver import *
import os
from paramiko import SSHClient, RSAKey, AutoAddPolicy
from StringIO import StringIO

class Ssh(Driver):
	DEFAULT_KEY_PATH = "~/.ssh/id_rsa"

	def __init__(self, host, username='root', password = None, key = None, port = 22, path = "/proc"):
		Driver.__init__(self)
		self._host = host
		self._username = username
		self._password = password
		self._port = port
		self._path = path

		self._client = None
		self._ftp = None

		if not password or key:
			self._key = RSAKey.from_private_key_file(os.path.expanduser(key or Ssh.DEFAULT_KEY_PATH))
		else:
			self._key = None

	def readFile(self, path):
		sftp = self._connectFtp()

		o = StringIO()
		for line in sftp.open(os.path.join(self._path, path)):
			o.write(line)

		return o.getvalue()

	def sh(self, cmd):
		client = self._connect()
		stdin, stdout, stderr = client.exec_command(cmd)
		return {
			"stdout": stdout.read(),
			"stderr": stderr.read(),
			"status": stdout.channel.recv_exit_status()
		}

	def _connect(self):
		if not self._client:
			client = SSHClient()
			client.set_missing_host_key_policy(AutoAddPolicy())
			client.connect(hostname = self._host, username=self._username, password=self._password, pkey=self._key, port=self._port, look_for_keys=False)
			self._client = client
		return self._client

	def _connectFtp(self):
		if not self._ftp:
			client = self._connect()
			self._ftp = client.open_sftp()
		return self._ftp

	def getHost(self):
		return self._host

def create(args):
	return Ssh(**args)