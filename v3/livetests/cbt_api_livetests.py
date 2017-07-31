
"""
CrossBrowserTesting.com API v3 Run Live Test sample script 

1. Install requests module: http://docs.python-requests.org/en/latest/user/install/#install
2. Run on Python 2.7 or greater
3. Run on Python Interpreter (command line)

"""
import requests, json, time
import httplib as http_client

http_client.HTTPConnection.debuglevel = 1

#set authentication info
username = "" #email address for your account
password = "" #authkey for your account

#set parameters we want for the live test
params = {}
params["browser"] = "chrome-latest"
params["url"] = "http://www.google.com"
params["api_timeout"] = 100 #number of second to allow test to run

class LiveTest:

    def __init__(self, username, password):

        self.auth = (username, password)
        self.baseUrl = "https://crossbrowsertesting.com/api/v3/livetests"
        self.currenTest = None
        self.currentVideo = None
        self.currentNetwork = None
        
    def callApi(self, url, method="GET", params={}):

        if method == "GET":
            response = requests.get(url,auth=self.auth,params=params)
        elif method == "POST":
            response = requests.post(url,auth=self.auth,params=params)
        elif method == "PUT":
            response = requests.put(url,auth=self.auth,params=params)
        elif method == "DELETE":
            response = requests.delete(url,auth=self.auth,params=params)
        else:
            response = requests.get(url,auth=self.auth,params=params)

        #print response.text
        result = json.loads(response.text)

        if "status" in result:
            print "http error " + str(result["status"]) + " : " + result["message"]
            quit()
        else:
            return result
    
    def startTest(self, params):
         self.currenTest = self.callApi(self.baseUrl, "POST", params)
         self.waitUntilRunning()

    def stopTest(self):
        url = self.baseUrl + "/" + str(self.currenTest["live_test_id"])
        self.callApi(url, "DELETE")

    def getLiveTestInfo(self):
        url = self.baseUrl + "/" + str(self.currenTest["live_test_id"])
        return self.callApi(url)

    def getLiveTestId(self):
        return self.currenTest["live_test_id"];

    def waitUntilRunning(self):

        tries = 0
        maxTries = 30
        print "waiting on live test state == running"
        while tries < maxTries:
            
            self.currentTest = self.getLiveTestInfo()
            if self.currentTest["state"] == "running":
                print "."
                break
            else:
                print ".",
                time.sleep(2)
                tries += 1

        if tries >= 30:
            print "Live Test not started after " + str(tries*2) + " seconds!"
            quit()

    def takeSnapshot(self):
        url = self.baseUrl + "/" + str(self.currenTest["live_test_id"]) + "/snapshots"
        self.callApi(url, "POST")

    def recordVideo(self):
        url = self.baseUrl + "/" + str(self.currenTest["live_test_id"]) + "/videos"
        self.currentVideo = self.callApi(url, "POST")

    def stopVideo(self):
        url = self.baseUrl + "/" + str(self.currenTest["live_test_id"]) + "/videos/" + self.currentVideo["hash"]
        self.callApi(url, "DELETE")

    def recordNetwork(self):
        url = self.baseUrl + "/" + str(self.currenTest["live_test_id"]) + "/networks"
        self.currentNetwork = self.callApi(url, "POST")

    def stopNetwork(self):
        url = self.baseUrl + "/" + str(self.currenTest["live_test_id"]) + "/networks/" + self.currentNetwork["hash"]
        self.callApi(url, "DELETE")


print "** Starting CrossBrowserTesting.com API v3 Run Live Test example **"

#create api object and set auth info
liveTest = LiveTest(username,password)

print "will launch browser " + params["browser"]
print "and open url " + params["url"]
print "live test will stop in " + str(params["api_timeout"]) +  " seconds"

#call new live test (will wait for test to launch before returning)
liveTest.startTest(params);
print "Live Test id is " + str(liveTest.getLiveTestId());
print "View Live Test on web here: https://app.crossbrowsertesting.com/livetests/run/" + str(liveTest.getLiveTestId());

print "starting video..."
liveTest.recordVideo()

print "starting network packet capture..."
liveTest.recordNetwork()

print "waiting a few seconds..."
time.sleep(5)

print "taking a snapshot..."
liveTest.takeSnapshot()

print "stopping network..."
liveTest.stopNetwork()

print "stopping video..."
liveTest.stopVideo()

print "stopping test..."
liveTest.stopTest()

print "View test results here: " + liveTest.currentTest["show_result_web_url"]
