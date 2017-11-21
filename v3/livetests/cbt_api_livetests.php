<?php

/* CrossBrowserTesting.com API v3 Run Live Test sample script 
* - requires PHP >= 5.2
* - run on the command line
* - requires libcurl package to be installed
*/

//set authentication info
$username = ""; //email address for your account
$password = ""; //authkey for your account

//set parameters we want for the live test
$params['browser'] = "chrome-latest";
$params['url'] = 'http://www.google.com';
$params['api_timeout'] = 100; //number of second to allow test to run

define ('EOL', "\n");


class LiveTest{

	public $baseUrl = "https://crossbrowsertesting.com/api/v3/livetests";

	public $currenTest = NULL;
	public $currentVideo = NULL;
	public $currentNetwork = NULL;

	function __construct($username, $password) {
		$this->user = $username;
		$this->pass = $password;
	}

	function startTest($params){
		$this->currenTest = $this->callApi($this->baseUrl, 'POST', $params);
		$this->waitUntilRunning();
	}

	function stopTest(){
		$url = $this->baseUrl. "/" . $this->currenTest->live_test_id;
		$this->callApi($url, 'DELETE');
	}

	function getLiveTestInfo(){
		$url = $this->baseUrl . "/" . $this->currenTest->live_test_id;
		return $this->callApi($url, 'GET');
	}

	function getLiveTestId(){
		return $this->currenTest->live_test_id;
	}

	function takeSnapshot(){
		$url = $this->baseUrl . "/" . $this->currenTest->live_test_id . "/snapshots";
		$this->callApi($url, 'POST');
	}

	function recordVideo(){
		$url = $this->baseUrl . "/" . $this->currenTest->live_test_id . "/videos";
		$this->currentVideo = $this->callApi($url, 'POST');
	}

	function stopVideo(){
		$url = $this->baseUrl . "/" . $this->currenTest->live_test_id . "/videos/" . $this->currentVideo->hash;
		$this->callApi($url, 'DELETE');
	}

	function recordNetwork(){
		$url = $this->baseUrl . "/" . $this->currenTest->live_test_id . "/networks";
		$this->currentNetwork = $this->callApi($url, 'POST');
	}

	function stopNetwork(){
		$url = $this->baseUrl . "/" . $this->currenTest->live_test_id . "/networks/" . $this->currentNetwork->hash;
		$this->callApi($url, 'DELETE');
	}

	function waitUntilRunning(){
		//waiting on test to be ready
		$tries = 0; $maxTries = 30; 
		print 'waiting on live test state == running'.EOL;
		while ($tries < $maxTries) {
			
			$this->currentTest = $this->getLiveTestInfo();
			if ($this->currentTest->state == 'running'){
				print EOL;
				break;
			}
			else {
				print '.';
				sleep(2);
				$tries++;
			}
		}

		if ($tries >= 30){
			die('Live Test not started after '.($tries*2).' seconds!');
		}
	}

	function callApi($api_url, $method = 'GET', $params = false)
	{
		$apiResult = new \stdClass();

	    $process = curl_init();

	    switch ($method)
	    {
	        case "POST":
	            curl_setopt($process, CURLOPT_POST, 1);

	            if ($params){
	                curl_setopt($process, CURLOPT_POSTFIELDS, $params);
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


print EOL.'** Starting CrossBrowserTesting.com API v3 Run Live Test example **'.EOL;

#create api object and set auth info
$liveTest = new LiveTest($username,$password);

print 'will launch browser '.$params['browser']. EOL;
print 'and open url '.$params['url']. EOL;
print 'live test will stop in '.$params['api_timeout'].' seconds'. EOL;

//call new live test (will wait for test to launch before returning)
$liveTest->startTest($params);
print 'Live Test id is '.$liveTest->getLiveTestId(). EOL;
print 'View Live Test on web here: https://app.crossbrowsertesting.com/livetests/run/'.$liveTest->getLiveTestId(). EOL;

print 'starting video...'.EOL;
$liveTest->recordVideo();

print 'starting network packet capture...'.EOL;
$liveTest->recordNetwork();

print 'waiting a few seconds...'.EOL;
sleep(2);

print 'taking a snapshot...'.EOL;
$liveTest->takeSnapshot();

print 'stopping network packet capture...'.EOL;
$liveTest->stopNetwork();

print 'stopping video...'.EOL;
$liveTest->stopVideo();

print 'stopping test...'.EOL;
$liveTest->stopTest();

print 'View test results here: '.$liveTest->currentTest->show_result_web_url.EOL;

?>