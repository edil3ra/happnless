
def login():
	### function lovingly borrowed from: https://github.com/tachang/makeithappn ###
	# OAuth endpoints given in the Facebook API documentation
	random_uuid = str(uuid.uuid4())
	authorization_base_url = 'https://www.facebook.com/dialog/oauth'
	token_url = 'https://graph.facebook.com/oauth/access_token'
	redirect_uri = 'https://%s.happn.com/' % random_uuid

	url = 'https://www.facebook.com/dialog/oauth?'
	params = {
	  'client_id' : '247294518656661',
	  'redirect_uri' : redirect_uri,
	  'scope' : 'user_birthday,email,user_likes,user_about_me,user_photos,user_work_history,user_friends',
	  'response_type' : 'token'
	}

	print "Please copy this into your browser:\n %s?%s" % ( authorization_base_url, urllib.urlencode(params) )

	# Get the authorization verifier code from the callback url
	redirect_response = raw_input('Paste the full redirect URL here:')

	# Parse the redirect response for the access_token
	o = urlparse(redirect_response)

	access_token = parse_qs(o.fragment)['access_token'][0]

	# client_id and client_secret can be obtained from a decompiled
	# happn\smali\com\ftw_and_co\happn\network\services\FacebookService.smali
	data = {
	  'client_id' :  'FUE-idSEP-f7AqCyuMcPr2K-1iCIU_YlvK-M-im3c',
	  'client_secret' :  'brGoHSwZsPjJ-lBk0HqEXVtb3UFu-y5l_JcOjD-Ekv',
	  'grant_type' : 'assertion',
	  'assertion_type' : 'facebook_access_token',
	  'assertion' : access_token,
	  'scope' : 'mobile_app'
	}

	url = 'https://connect.happn.fr/connect/oauth/token'

	r = requests.post(url, headers=preAuthHeaders, data=data, verify=False)
	user_info = r.json()

	myID = user_info['user_id']
	OAuth = user_info['access_token']

	file = open("key", "w")
	file.write(OAuth)
	file.close()
