import sys

def __writeLine(msg):
	sys.stderr.write(msg + "\n")

def printWarn(msg):
	__writeLine("[WARN] " + str(msg))

def printError(msg):
	__writeLine("[ERRO] " + str(msg))

def printInfo(msg):
	__writeLine("[INFO] " + str(msg))

