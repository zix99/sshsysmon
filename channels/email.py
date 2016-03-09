from channel import Channel
import smtplib


class Email(Channel):
	DEFAULT_SUBJECT = "[ALERT] {server} failed on {alert}"
	DEFAULT_BODY = """
There was an alert on your server.

Sincerely,
SshSysMon
"""

	def __init__(self, toAddr, fromAddr = None, host = 'localhost', port=25, body=DEFAULT_BODY, subject = DEFAULT_SUBJECT, username = None, password = None, tls = False, ssl = False):
		self._to = toAddr
		self._from = fromAddr or toAddr
		self._subject = subject
		self._body = body
		self._host = host
		self._port = port
		self._username = username
		self._password = password
		self._tls = tls
		self._ssl = ssl

	def notify(self, model):
		try:
			fromAddr = self._from
			toAddr = self._to.split()
			subj = self._subject.format(**model)

			message = "From: {frm}\nTo: {to}\nSubject: {subject}\n\n{body}".format(frm=fromAddr, to=toAddr, subject=subj, body=self._body)

			if self._ssl:
				server = smtplib.SMTP_SSL(self._host, self._port)
			else:
				server = smtplib.SMTP(self._host, self._port)

			server.ehlo()

			if self._username:
				if (self._tls):
					server.starttls()
				server.login(self._username, self._password)

			server.sendmail(fromAddr, toAddr, message)
			server.close()
		except Exception, e:
			print "There was an error sending an email %s" % e
