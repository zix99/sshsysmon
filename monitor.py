

def evalCriteria(statement, data):
	for k,v in data.iteritems():
		exec("%s = %s" % (k,v))
	return eval(statement)





