from twitter import oauth_dance
from twitter.oauth import read_token_file
import twitter
import os

CLIENT_KEY = "TIHKzKDH42F8oxekg40wA"
CLIENT_SECRET = "vsSO7ZK2Z37sb0ExiroCO8HzEompudXvl2LlZtnUK8o"

def oauthToken(oauth_filename=os.sep.join([os.getenv('HOME'),".twitter_oauth"])):
	if (not os.path.exists(oauth_filename)):
		oauth_dance("the Command-Line Tool", CLIENT_KEY, CLIENT_SECRET,oauth_filename)
	oauth_token, oauth_token_secret = read_token_file(oauth_filename)
	return twitter.OAuth(oauth_token,oauth_token_secret,CLIENT_KEY,CLIENT_SECRET)

if __name__ == '__main__':
	print oauthToken()

# index = []
# def loadTokensIndex(loc):
#   f = file(loc,"r")
#   for line in f.readlines():
#     if line.startswith("#"): continue
#     parts = [x.strip() for x in line.split(",")]
#     (consumer_key,consumer_secret,auth_key,auth_secret) = parts
#     tokens = dict()
#     tokens["CLIENT_KEY"] = consumer_key
#     tokens["CLIENT_SECRET"] = consumer_secret
#     tokens["ATOKEN_KEY"] = auth_key
#     tokens["ATOKEN_SECRET"] = auth_secret
#     index = index + [tokens]
#   return index

# def request(url,http_method="GET",post_body=None,http_headers=None):
#   consumer=oauth2.Consumer(key=tokens["CLIENT_KEY"],secret=tokens["CLIENT_SECRET"])
#   token=oauth2.Token(key=tokens["ATOKEN_KEY"],secret=tokens["ATOKEN_SECRET"])
#   client=oauth2.Client(consumer,token)
#   resp,content=client.request(url,method="GET",body=None,headers=None,force_auth_header=True)
#   return content

# CONF_DIR = os.getenv('HOME') # where to find the configuration
# CONSUMER = (int(sys.argv[2]) if len(sys.argv) >= 3 else 0)
# tokensIndex = loadTokensIndex(os.sep.join([CONF_DIR,".twittertokens"]))
# tokens = tokensIndex[CONSUMER]

# print request(sys.argv[1])
