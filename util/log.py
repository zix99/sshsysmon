import sys

def __writeLine(msg):
	sys.stderr.write(msg + "\n")

def printWarn(msg):
	__writeLine("[WARN] " + msg)

def printError(msg):
	__writeLine("[ERRO] " + msg)

def printInfo(msg):
	__writeLine("[INFO] " + msg)

