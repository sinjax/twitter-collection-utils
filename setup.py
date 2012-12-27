#!/usr/bin/env python

from setuptools import setup

setup(
	name='twitter_collection_utils',
	version='1.0',
	description='stdin to kestrel queues',
	author='Daniel Preotiuc',
	author_email='daniel@dcs.shef.ac.uk',
	url='github.com/danielpreotiuc/twitter-collection-utils',
	packages=['twitter_collection_utils'],
	scripts=['bin/dedupl.sh',"bin/tcufollow"],
	dependency_links = ['https://github.com/brosner/python-oauth2/tarball/master#egg=oauth2-1.0.2'],
	install_requires=['oauth2','twitter'],
)