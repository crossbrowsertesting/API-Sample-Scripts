
"""
CrossBrowserTesting.com API v3 Run Screenshots sample script 

1. Install requests module: http://docs.python-requests.org/en/latest/user/install/#install
2. Run on Python 2.7 or greater
3. Run on Python Interpreter (command line)

"""
import requests, json, time

#import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1

#set authentication info
username = "" #email address for your account
password = "" #authkey for your account

EOL = "\n"
TAB = "\t"

class ScreenshotTestApi:

    def __init__(self, username, password, screenshot_test_id=None):

        self.auth = (username, password)
        self.baseUrl = "https://crossbrowsertesting.com/api/v3/screenshots"
        self.currentTest = None
        self.allTests = []
        self.recordCount = 0

        #if test id provided initialize this test to that test data
        if screenshot_test_id:
            url = self.baseUrl + "/" + str(screenshot_test_id)
            self.currentTest = self.callApi(url)
    
    def startNewTest(self, params):
         self.currentTest = self.callApi(self.baseUrl, "POST", params)

    def updateTestInfo(self):
        url = self.baseUrl + "/" + str(self.getTestId())
        return self.callApi(url)

    def getTestId(self):
        return self.currentTest["screenshot_test_id"]

    def printTestBrowsers(self):
        if (self.currentTest):
            for result in self.currentTest["versions"][0]["results"]:
                print result["os"]["name"] + TAB + result["browser"]["name"] + TAB + result["resolution"]["name"]

    def isTestComplete(self):
        self.currentTest = self.updateTestInfo()
        return not self.currentTest["versions"][0]["active"]

    def getScreenshotBrowsers(self):
        url = self.baseUrl + "/browsers"
        return self.callApi(url)

    def getAllTests(self, params={}):
        result = self.callApi(self.baseUrl,"GET", params)
        self.recordCount = result["meta"]["record_count"]
        self.allTests = result["screenshots"]
        return self.allTests

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

        print response.text
        result = json.loads(response.text)

        if "status" in result:
            print "http error " + str(result["status"]),
            if "message" in result:
                print " : " + result["message"]
            quit()
        else:
            return result
    

def runNewTestAndWait():

    print EOL + "** Starting CrossBrowserTesting.com API v3 Run Screenshot Test example **"

    #set parameters we want for the screenshot test
    params = {}
    #params["url"] = "http://www.google.com"
    params["url"] = "http://www.midsouthproducts.com/collections/elvis-presley/products/frame-elvis-dancing-pewter"

    #set browsers
    params["browsers"] = []
    #params["browsers"].append("Win7x64|IE10|1400x1050")
    #params["browsers"].append("Win7x64|chrome-latest|1400x1050")
    #params["browsers"].append("Win7x64|ff-latest|1400x1050")
    #params["browsers"].append("Mac10.9|chrome-latest-1")

    #other options
    params["browser_list_name"] = "Popular Browsers"
    params["login"] = "www.midsouthproducts.com login"
    ##params["login"] = "mydomain.com login" #valid only if you've created a login profile with this name
    ##params["basic_username"] = "username" #for basic auth urls only
    ##params["basic_password"] = "password" #for basic auth urls only
    params["delay"] = 4 #delay for number of seconds to wait after page is loaded to start capturing screenshots

    #create api object and set auth info
    screenshot = ScreenshotTestApi(username,password)

    print "starting new screenshot test for " + params["url"]
    screenshot.startNewTest(params)

    print "screenshot_test_id is " + str(screenshot.getTestId())
    print "view Screenshot Test on web here: https://app.crossbrowsertesting.com/screenshots/" + str(screenshot.getTestId())

    print EOL + "browsers to be tested are: "
    screenshot.printTestBrowsers()

    print EOL + "waiting on test to complete"
    tries = 0
    maxTries = 100
    while tries < maxTries:
        
        if screenshot.isTestComplete():
            print "screenshot test complete"
            break
        else:
            time.sleep(2)
            tries += 1

    if tries >= maxTries:
        print "screenshot did not complete after " + str(tries*2) + " seconds!"
        quit()

def runNewTest():

    print EOL + "** Starting CrossBrowserTesting.com API v3 Run Screenshot Test example **"

    #set parameters we want for the screenshot test
    params = {}
    #params["url"] = "http://212.121.155.205/WFRM-QA-Support/CBTWebPage/600382124/WOFF2.html"
    params["url"] = "http://www.google.com"
    #params["url"] = "http://www.midsouthproducts.com/collections/elvis-presley/products/frame-elvis-dancing-pewter"

    #set browsers
    # params["browsers"] = []
    # params["browsers"].append("Win8.1|chrome-latest|2560x1600")
    # params["browsers"].append("Win8.1|chrome-latest|1920x1080")
    #params["browsers"].append("Win7x64|ff-latest|1400x1050")
    #params["browsers"].append("Win7x64|ff-latest|1400x1050")
    #params["browsers"].append("Mac10.9|chrome-latest")

    #other options
    params["browser_list_name"] = "simple-list"
    #params["login"] = "www.midsouthproducts.com login"
    ##params["login"] = "mydomain.com login" #valid only if you've created a login profile with this name
    ##params["basic_username"] = "username" #for basic auth urls only
    ##params["basic_password"] = "password" #for basic auth urls only
    #params["delay"] = 4 #delay for number of seconds to wait after page is loaded to start capturing screenshots

    #create api object and set auth info
    screenshot = ScreenshotTestApi(username,password)

    print "starting new screenshot test for " + params["url"]
    screenshot.startNewTest(params)

    print "screenshot_test_id is " + str(screenshot.getTestId())
    print "view Screenshot Test on web here: https://app.crossbrowsertesting.com/screenshots/" + str(screenshot.getTestId())

    print EOL + "browsers to be tested are: "
    screenshot.printTestBrowsers()

def viewTestHistory():

    print EOL + "** Starting CrossBrowserTesting.com API v3 View Screenshot History example **"

    #set paging options
    params = {}
    params["start"] = 0 #start with the last test run
    params["num"] = 20 #how many to retrieve

    #filter results
    params["url"] = "google" #filter for only tests run that have 'google' somewhere in the URL
    params["start_date"] = "2014-06-01" #fitler to only tests run within a date range
    params["end_date"] = "2014-10-01"
    params["archived"] = False #only include screenshot tests that are not archived

    #create api object and set auth info
    print "retrieving test history"
    screenshots = ScreenshotTestApi(username,password)
    allTests = screenshots.getAllTests(params)

    #show total number of tests
    print "There are " + str(screenshots.recordCount) + " tests for  the filters provided, showing " + str(len(allTests))

    for i in range(len(allTests)):
        test = allTests[i]
        version = test["versions"][0]
        start_date = version["start_date"]
        print str(i+1) + TAB + start_date + TAB + str(test["screenshot_test_id"]) + TAB + test["url"]

def listScreenshotBrowsers():
    print EOL + "** Starting CrossBrowserTesting.com API v3 List Screenshot Browsers example **"

    #create api object and set auth info
    screenshotApi = ScreenshotTestApi(username,password)
    oss = screenshotApi.getScreenshotBrowsers()

    for os in oss:
        for browser in os["browsers"]:
            print os["name"] + TAB + browser["name"] + TAB + os["api_name"] + "|" + browser["api_name"]

# uncomment a function to run
# listScreenshotBrowsers()
# runNewTest()
# viewTestHistory()