import time
import sys
import twitter
import json
import cPickle as pickle
import os
import datetime
from .oauth import oauthToken
from optparse import OptionParser

def main():
	parser = OptionParser()
	parser.add_option("-t", "--tokens-file", dest="TOKENS_FILE",help="The twitter auth tokens",default=os.sep.join([os.getenv('HOME'),".twitter_oauth"]))
	parser.add_option("-s", "--step", dest="STEP",help="Number of tweets retrieved per call",default=200)
	parser.add_option("-w", "--step-wait", dest="WAIT_CALL",help="Time to wait between calls",default=60)
	parser.add_option("-f", "--fail-wait", dest="WAIT_PERIOD",help="Time to wait between failures",default=2)
	parser.add_option("-o", "--output", dest="OUTPUT",help="Output directory (containing a file per day)",default="timeline_out")


	(options, arguments) = parser.parse_args()

	o = options.OUTPUT
	if os.path.exists(o):
		if not os.path.isdir(o):
			print >> sys.stderr,"output exists, but is not a directory!"
	else:
		os.makedirs(o)

	c_tw=twitter.Twitter(
	  domain='api.twitter.com',
	  api_version="1",
	  auth=oauthToken(options.TOKENS_FILE)
	)

	WAIT_PERIOD = float(options.WAIT_PERIOD) # time until retry for a failed Twitter API call
	WAIT_CALL = float(options.WAIT_CALL) # frequency of checking the timeline (I think it's useless checking more often than 60 seconds)
	STEP = int(options.STEP) # number of tweets retrieved per call; should always be 200 (maximum)

	new_sid=1
	sid=1
	lid=1
	d=datetime.datetime.now()
	da=d.day
	FNAME=str(d.year)+'-'+str(d.month)+'-'+str(d.day)
	FNAME=os.path.sep.join([o,FNAME])
	fout=open(FNAME,"w")
	while True:
		if not da==datetime.datetime.now().second:
			d=datetime.datetime.now()
			da=d.day	 
			fout.close()
			os.system("lzop -9U "+FNAME)
			FNAME=str(d.year)+'-'+str(d.month)+'-'+str(d.day)
			FNAME=os.path.sep.join([o,FNAME])
			fout=open(FNAME,"w")
		try:
			tweets=c_tw.statuses.home_timeline(count=STEP,since_id=sid)
		except twitter.api.TwitterError, e:
			print >> sys.stderr, "An error: %s, waiting %s"%(e,WAIT_PERIOD)
			time.sleep(WAIT_PERIOD)
			continue
		except:
			continue
		if len(tweets)==0:
			time.sleep(WAIT_CALL)
			continue
	# this is the newset tweet we have, next time download only newer stuff
		new_sid=tweets[0]['id']
		lid=tweets[len(tweets)-1]['id']
		tlist=tweets
		while lid>sid:
	# we have more than STEP tweets in the sleeping time, go back in time until sid and get them
			try:
				tweets=c_tw.statuses.home_timeline(count=STEP,max_id=lid-1,since_id=sid)
			except twitter.api.TwitterError, e:
				time.sleep(WAIT_PERIOD)
				break;	
			if len(tweets)==0:
				break
			lid=tweets[len(tweets)-1]['id']
			tlist=tlist+tweets
	# print the tweets we got in reverse order so that we mentain the order of timestamps
		tlist.reverse()
		for tweet in tlist:
			print >> fout, json.dumps(tweet)
		sid=new_sid	
		time.sleep(WAIT_CALL)

try:
	main()
except KeyboardInterrupt:
	pass
