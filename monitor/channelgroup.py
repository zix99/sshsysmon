import channels

class ChannelGroup:
	def __init__(self, channelList):
		self._channels = []

		for channel in channelList:
			channel_type = channel.get('type')
			channel_config = channel.get('config', {})

			try:
				inst = channels.createChannel(channel_type, channel_config)
				self._channels.append(inst)
			except Exception, e:
				print "Error notifying channel: %s" % e

	def notify(self, alert, data = {}):
		payload = data.copy()
		payload.update({
			"server" : alert.serverName,
			"alert" : alert.name,
			"statement" : alert.statement
			})

		for channel in self._channels:
			try:
				channel.notify(payload)
			except Exception, e:
				print "Error notifying channel %s: %s" % (channel, e)