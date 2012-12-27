#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name='twitter_collection_utils',
	version='1.0',
	description='stdin to kestrel queues',
	author='Daniel Preotiuc',
	author_email='daniel@dcs.shef.ac.uk',
	url='github.com/danielpreotiuc/twitter-collection-utils',
	packages=['twitter_collection_utils'],
	scripts=['bin/dedupl.sh'],
	requires=['oauth2',],
)