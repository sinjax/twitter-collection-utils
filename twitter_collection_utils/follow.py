import twitter
import time
import os
import sys
from .oauth import oauthToken
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-u", "--user-file", dest="USER_FILE",help="The file containing the users to follow",default=None)
parser.add_option("-t", "--tokens-file", dest="TOKENS_FILE",help="The twitter auth tokens",default=os.sep.join([os.getenv('HOME'),".twitter_oauth"]))
parser.add_option("-i", "--iterations", dest="ITER",help="Number of iterations to add the users in",default=10)
parser.add_option("-w", "--wait", dest="WAIT",help="Time to wait between iterations",default=3600)

(options, arguments) = parser.parse_args()

USER_FILE = options.USER_FILE
ITER = options.ITER
WAIT = options.WAIT

c_tw=twitter.Twitter(
  domain='api.twitter.com',
  api_version="1.1",
  auth=oauthToken(options.TOKENS_FILE)
)

users=[]
if USER_FILE:
	if os.path.exists(USER_FILE):
		f=open(USER_FILE,'r')
		for line in f:
			users.append(line.strip())
		f.close()
	else:
		print >>sys.stderr,"File: '%s' not found, exiting"%USER_FILE
		sys.exit(1)
else:
	for line in sys.stdin.readlines():
		users.append(line.strip())

parts = [i for i in xrange(0,len(users),ITER)]

for x in parts:
	part = users[x:x+ITER]
	print "Following %d people" % len(part)
	for person in part:
		try:
			c_tw.friendships.create(screen_name=person)
			print "Following %s" % person
		except twitter.api.TwitterError, e:
			print "Could not add %s" % person
		if x is not parts[-1]:
			print "Waiting %d seconds" % time
			WAIT.sleep(WAIT)
