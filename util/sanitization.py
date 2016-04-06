import re

def sanitize(s):
	return re.sub('[^0-9a-zA-Z]+', '_', s)
