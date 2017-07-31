<?php

/* CrossBrowserTesting.com API v3 Screenshots sample script 
* - requires PHP >= 5.2
* - run on the command line
* - requires libcurl package to be installed
*/

//set authentication info
$username = ""; //email address for your account
$password = ""; //authkey for your account

define ('EOL', "\n");
define ('TAB', "\t");


class ScreenshotTestApi{

	public $baseUrl = "https://crossbrowsertesting.com/api/v3/screenshots";

	public $currentTest = NULL;
	public $allTests = array();
	public $recordCout = 0;

	function __construct($username, $password, $screenshot_test_id=NULL) {
		$this->user = $username;
		$this->pass = $password;

		//if test id provided initialize this test to that test data
        if ($screenshot_test_id){
            $url = $this->baseUrl . "/" . $screenshot_test_id;
            $this->currentTest = $this->callApi($url);
        }
	}

	function startNewTest($params){
		$this->currentTest = $this->callApi($this->baseUrl, 'POST', $params);
	}

	function updateTestInfo(){
		$url = $this->baseUrl . "/" . $this->getTestId();
		return $this->callApi($url, 'GET');
	}

	function getTestId(){
		return $this->currentTest->screenshot_test_id;
	}

	function printTestBrowsers(){
		if ($this->currentTest){
			foreach ($this->currentTest->versions[0]->results as $result) {
				print $result->os->name  . TAB . $result->browser->name . TAB . $result->resolution->name . EOL;
			}
		}
	}

	function isTestComplete(){
		$this->currentTest = $this->updateTestInfo();
		return !$this->currentTest->versions[0]->active;
	}

	function getScreenshotBrowsers(){
		$url = $this->baseUrl . "/browsers";
		return $this->callApi($url, 'GET');
	}

	function getAllTests($params = false){
		$url = $this->baseUrl;
		$result = $this->callApi($url, 'GET',$params);
		$this->recordCount = $result->meta->record_count;
        $this->allTests = $result->screenshots;
        return $this->allTests;
	}

	function callApi($api_url, $method = 'GET', $params = false){
		$apiResult = NULL;

	    $process = curl_init();

	    switch ($method){
	        case "POST":
	            curl_setopt($process, CURLOPT_POST, 1);

	            if ($params){
	                curl_setopt($process, CURLOPT_POSTFIELDS, http_build_query($params));
	                curl_setopt($process, CURLOPT_HTTPHEADER, array('User-Agent: php')); //important
	            }
	            break;
	        case "PUT":
	            curl_setopt($process, CURLOPT_CUSTOMREQUEST, "PUT");
	            if ($params){
	                curl_setopt($process, CURLOPT_POSTFIELDS, http_build_query($params));
	                curl_setopt($process, CURLOPT_HTTPHEADER, array('User-Agent: php')); //important
	            }
	            break;
	         case 'DELETE':
	         	curl_setopt($process, CURLOPT_CUSTOMREQUEST, "DELETE");
	         	break;
	        default:
	            if ($params){
	                $api_url = sprintf("%s?%s", $api_url, http_build_query($params));
	            }
	    }

	    // Optional Authentication:
	    curl_setopt($process, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
	    curl_setopt($process, CURLOPT_USERPWD, $this->user . ":" . $this->pass);

	    curl_setopt($process, CURLOPT_URL, $api_url);
	    curl_setopt($process, CURLOPT_RETURNTRANSFER, 1);
	    curl_setopt($process, CURLOPT_TIMEOUT, 30);

	    $apiResult->content = curl_exec($process);
		$apiResult->httpResponse = curl_getinfo($process);	
		$apiResult->errorMessage =  curl_error($process);
		$apiResult->params = $params;

		curl_close($process);

		//print_r($apiResult);

		$paramsString = $params ? http_build_query($params) : '';
		$response = json_decode($apiResult->content);

		if ($apiResult->httpResponse['http_code'] != 200){
			$message = 'Error calling "' . $apiResult->httpResponse['url'] . '" ';
			$message .= (isset($paramsString) ? 'with params "'.$paramsString.'" ' : ' ');
			$message .= '. Returned HTTP status ' . $apiResult->httpResponse['http_code'] . ' ';
			$message .= (isset($apiResult->errorMessage) ? $apiResult->errorMessage : ' ');
			$message .= (isset($response->message) ? $response->message : ' ');
			die($message);
		}
		else {
			$response = json_decode($apiResult->content);
			if (isset($response->status)){
				die('Error calling "' . $apiResult->httpResponse['url'] . '"' .(isset($paramsString) ? 'with params "'.$paramsString.'"' : '') . '". ' . $response->message);			
			}
		}

	    return $response;
	}
}



function runNewTest(){
	global $username, $password;

	print EOL.'** Starting CrossBrowserTesting.com API v3 Run Screenshot Test example **'.EOL;

	//set parameters we want for the screenshot test
    $params["url"] = "http://www.google.com";

    //set browsers
    $params["browsers"] = array();
    $params["browsers"][] = "Win7x64|IE11|1400x1050";
    $params["browsers"][] = "Mac10.9|chrome-latest";
    $params["browsers"][] = "Win10|ff-latest";

	$screenshot = new ScreenshotTestApi($username,$password);

	print "starting new screenshot test for " . $params["url"].EOL;
    $screenshot->startNewTest($params);

    print "screenshot_test_id is " . $screenshot->getTestId().EOL;
    print "view Screenshot Test on web here: https://app.crossbrowsertesting.com/screenshots/" . $screenshot->getTestId().EOL;

    print EOL."browsers to be tested are: ".EOL;
    $screenshot->printTestBrowsers();

    print "waiting on test to complete".EOL;
    $tries = 0;
    $maxTries = 100;
    while ($tries < $maxTries){
        
        if ($screenshot->isTestComplete()){
            print "screenshot test complete".EOL;
            break;
        }
        else{
            sleep(2);
            $tries += 1;
        }
	}
    if ($tries >= $maxTries){
        die("screenshot did not complete after " . str($tries*2) . " seconds!".EOL);
    }
}

function viewTestHistory(){
	global $username, $password;

	print EOL."** Starting CrossBrowserTesting.com API v3 View Screenshot History example **".EOL;

	//set paging options
	$params["start"] = 0; //start with the last test run
    $params["num"] = 20; //how many to retrieve

    //filter results
    $params["url"] = "google"; //filter for only tests run that have 'google' somewhere in the URL
    $params["start_date"] = "2014-06-01"; //fitler to only tests run within a date range
    $params["end_date"] = "2014-10-01";
    $params["archived"] = false; //only include screenshot tests that are not archived

    //create api object and set auth info
    print "retrieving test history".EOL;
    $screenshots = new ScreenshotTestApi($username,$password);
    $allTests = $screenshots->getAllTests($params);

    //show total number of tests
    print "There are " . $screenshots->recordCount . " tests for  the filters provided, showing " . count($allTests) . EOL;

    //print out results
    for ($i=0; $i<count($allTests); $i++){
        $test = $allTests[$i];
        $version = $test->versions[0];
        $start_date = $version->start_date;
        print ($i+1) . TAB . $start_date . TAB . $test->screenshot_test_id  . TAB . $test->url.EOL;
    }

}

function listScreenshotBrowsers(){
    print EOL."** Starting CrossBrowserTesting.com API v3 List Screenshot Browsers example **".EOL;

    //create api object and set auth info
    $screenshotApi = new ScreenshotTestApi($username,$password);
    $oss = $screenshotApi->getScreenshotBrowsers();

    foreach ($oss as $os){
        foreach($os->browsers as $browser){
            print $os->name . TAB . $browser->name . TAB . $os->api_name . "|" . $browser->api_name.EOL;
        }
    }
}

// uncomment a function to run
// listScreenshotBrowsers();
// runNewTest();
// viewTestHistory();

?>