import re

# Replaces any non-alphanumeric characters with a _
def sanitize(s, repl='_'):
	return re.sub('[^0-9a-zA-Z]+', repl, s)
