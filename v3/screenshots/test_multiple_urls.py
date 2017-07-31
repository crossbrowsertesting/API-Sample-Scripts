import urllib2
import string
# create a password manager
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

# Add the username and password.
# If we knew the realm, we could use it instead of None.
top_level_url = "https://crossbrowsertesting.com/api/v3/screenshots"
password_mgr.add_password(None, top_level_url, USERNAME, AUTHKEY)

handler = urllib2.HTTPBasicAuthHandler(password_mgr)

# create "opener" (OpenerDirector instance)
opener = urllib2.build_opener(handler)

# use the opener to fetch a URL
opener.open("https://crossbrowsertesting.com/api/v3/screenshots")

# Install the opener.
# Now all calls to urllib2.urlopen use our opener.
urllib2.install_opener(opener)



with open("urls.txt") as f:
    for line in f:
        data = '{"browsers": ["Win8.1|chrome-latest","Win10|ff-latest"], "url": '+ "\""+ string.strip(line) +"\"" + '}'
    req = urllib2.Request(top_level_url, data, {'Content-Type': 'application/json'})
    urllib2.urlopen(req)
