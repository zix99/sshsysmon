#!/usr/bin/env python
from setuptools import setup, find_packages

readme = open('README.md').read()
try:
	import pypandoc, re
	readme = re.sub('\!\[.+\]\(.+\)', '', readme) # Remove embedded pictures
	readme = pypandoc.convert(readme, 'rst', format='md')
except Exception as e:
	print "Expected pypandoc and pandoc to be installed!"
	print e

setup(name="SshSysMon",
	packages=find_packages(),
	package_data={
		'': ['LICENSE.txt', 'README.md', 'examples/*'],
		'sshsysmon.templates' : ['*.md', '*.hb'],
		'sshsysmon' : [
			'drivers/*.md', 'drivers/*.py',
			'channels/*.md', 'channels/*.py',
			'inspectors/*.md', 'inspectors/*.py'
			],
		},
	version="0.2.2",
	description="Ssh Unix System Monitoring",
	long_description=readme,
	author="Chris LaPointe",
	author_email="chris@zdyn.net",
	url="https://github.com/zix99/sshsysmon",
	license="MIT",
	keywords=["monitoring", "ssh", "linux", "unix"],
	install_requires=[
		"paramiko==1.16.0",
		"pyaml==15.8.2",
		"pybars3==0.9.1"
		],
	scripts=["sshmon"],
	zip_safe=False
	)
