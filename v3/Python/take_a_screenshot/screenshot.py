#!/usr/local/bin/python
from requests import post, get, delete
from time import sleep
 
username = ""
apikey = ""
 
print "Launching the test"
test = post(
            'https://%s:%s@crossbrowsertesting.com/api/v3/livetests' % (username, apikey),
        data = { 'url': "https://frederik-braun.com", 'browser': "MblFF36" }
            )
live_test_id = test.json()["live_test_id"]
print "Test id is: %s" % live_test_id
running = False
count = 12
while not running and count > 0:
    print "Waiting for the test to load"
    test = get('https://%s:%s@crossbrowsertesting.com/api/v3/livetests/%s' % (username, apikey, live_test_id))
    state = test.json()["state"]
    if state == "running":
        running = True
    elif count == 0:
        print "60 second timeout waiting for test to load"
        delete('https://%s:%s@crossbrowsertesting.com/api/v3/livetests/%s' % (username, apikey, live_test_id))
        exit(1)
    sleep(5) # avoid hammering the api
    count = count - 1
print "Done loading"
sleep(10) # give the browser time to load
print "Taking snapshot"
post('https://%s:%s@crossbrowsertesting.com/api/v3/livetests/%s/snapshots' % (username, apikey, live_test_id))
sleep(3)
print "Stopping the test"
delete('https://%s:%s@crossbrowsertesting.com/api/v3/livetests/%s' % (username, apikey, live_test_id))