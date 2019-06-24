#!/usr/bin/env python
from setuptools import setup, find_packages
import re

readme = open('README.md').read()
readme = re.sub('\!\[.+\]\(.+\)', '', readme) # Remove embedded pictures

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
	version="0.2.3",
	description="Ssh Unix System Monitoring",
	long_description=readme,
	long_description_content_type='text/markdown',
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
