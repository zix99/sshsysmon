
class ByteSize:
	SIZE_SUFFIX = ["B", "KB", "MB", "GB", "TB", "PB"]

	def __init__(self, byteCount, unit = "B"):
		self._bytes = int(float(byteCount) * 1024**ByteSize.SIZE_SUFFIX.index(unit.upper()))

	@property
	def bytes(self):
		return self._bytes

	@property
	def b(self):
		return self._bytes

	@property
	def kb(self):
	    return self._bytes / 1024.0

	@property
	def mb(self):
		return self._bytes / 1024.0 / 1024.0

	@property
	def gb(self):
		return self._bytes / 1024.0 / 1024.0 / 1024.0

	@property
	def tb(self):
		return self._bytes / 1024.0 / 1024.0 / 1024.0 / 1024.0

	@property
	def pb(self):
		return self._bytes / 1024.0 / 1024.0 / 1024.0 / 1024.0 / 1024.0

	def __json__(self):
		return self._bytes

	def __int__(self):
		return self._bytes

	def __str__(self):
		curr = self._bytes
		idx = 0
		while curr > 1024 and idx < len(ByteSize.SIZE_SUFFIX) - 1:
			curr /= 1024.0
			idx += 1
		return "%0.2f %s" % (curr, ByteSize.SIZE_SUFFIX[idx])

	def __repr__(self):
		return "< %d bytes >" % self._bytes

	def __lt__(self, other): return int(self) < int(other)
	def __le__(self, other): return int(self) <= int(other)
	def __eq__(self, other): return int(self) == int(other)
	def __ne__(self, other): return int(self) != int(other)
	def __gt__(self, other): return int(self) > int(other)
	def __ge__(self, other): return int(self) >= int(other)