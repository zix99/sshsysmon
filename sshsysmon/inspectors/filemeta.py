from inspector import Inspector
from StringIO import StringIO
from fnmatch import fnmatch
from lib.util import ByteSize, TimeSpan
from datetime import datetime, timedelta

"""
Description:
	Retrieve metadata for one or more files
Constructor:
	- path: Path of the files to look
	- match: Pattern to match for filename (Default: None)
	- maxDepth: The depth in the file system to search (set to 1 for no recurse)
	- minDepth: The minimum depth to start looking for files
Metrics:
	- count: Number of files that match
	- oldest: The TimeSpan object of the oldest file
	- newest: The TimeSpan object of the newest file
	- largest: ByteSize of the largest file
	- smallest: ByteSize of smallest file
	- files: Array of files
		- path: Path to the file
		- size: ByteSize of the file
		- last_access: access date
		- last_modified: last modified time
		- age: TimeSpan since last modified
"""
class FileMeta(Inspector):
	def __init__(self, driver, path, match = None, maxDepth = None, minDepth = None):
		self._driver = driver
		self._path = path
		self._match = match
		self._maxDepth = maxDepth
		self._minDepth = minDepth

	def getMetrics(self):
		shFind = ["find", "\"%s\"" % self._path, "-type", "f"]
		if self._maxDepth != None: shFind.extend(["-maxdepth", self._maxDepth])
		if self._minDepth != None: shFind.extend(["-mindepth", self._minDepth])

		cmd = str.join(' ', map(str, shFind)) + " | xargs stat -t"

		stats = self._driver.sh(cmd)

		files = stats['stdout'].splitlines()

		metrics = {
			'count': len(files),
			'files' : [],
			'oldest' : TimeSpan(0),
			'newest' : TimeSpan(0),
			'largest' : ByteSize(0),
			'smallest' : ByteSize(0),
			'size' : ByteSize(0)
		}

		for file in files:
			parts = file.split()
			if len(parts) >= 12:
				filename = parts[0]

				if self._match == None or fnmatch(filename, self._match):
					# 0 %n File name
					# 1 %s Size, bytes
					# 2 %b Numer of blocks
					# 3 %f raw mode
					# 4 %u User ID
					# 5 %g group
					# 6 %D device
					# 7 %i inode
					# 8 %h Numer of hard links
					# 9 %t Major device
					# 10 %T minor
					# 11 %X Time of last access
					# 12 %Y - last modified
					# 13 %Z - last status change
					# 14 %W file birth

					now = datetime.now()
					access_time = datetime.fromtimestamp(int(parts[11]))
					modified_time = datetime.fromtimestamp(int(parts[12]))

					metrics['files'].append({
						'path' : filename,
						'size' : ByteSize(parts[1]),
						'last_access' : access_time,
						'last_modified' : modified_time,
						'age' : TimeSpan.fromTimeDelta(now - modified_time)
					})

		if len(metrics['files']) > 0:
			metrics['oldest'] = max(map(lambda x: x['age'], metrics['files']))
			metrics['newest'] = min(map(lambda x: x['age'], metrics['files']))
			metrics['largest'] = max(map(lambda x: x['size'], metrics['files']))
			metrics['smallest'] = min(map(lambda x: x['size'], metrics['files']))
			metrics['size'] = ByteSize(sum(map(lambda x: int(x['size']), metrics['files'])))

		return metrics

	def getSummary(self):
		metrics = self.getMetricsCached()

		o = StringIO()

		o.write("Count: %s\n" % len(metrics['files']))
		o.write("Size: %s\n" % metrics['size'])
		o.write("Oldest: %s\n" % metrics['oldest'])
		o.write("Newest: %s\n" % metrics['newest'])
		o.write("Largest: %s\n" % metrics['largest'])
		o.write("Smallest: %s\n" % metrics['smallest'])

		return o.getvalue()

	def getName(self):
		return "Files: %s" % (self._path)

def create(driver, args):
	return FileMeta(driver, **args)