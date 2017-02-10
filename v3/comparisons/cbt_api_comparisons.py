import requests
from requests.auth import HTTPBasicAuth


baseUrl = "https://crossbrowsertesting.com/api/v3/screenshots"


class CBT_Comparisons_API:
	def __init__(self, user, auth):
		self.user = user
		self.auth = auth
		self.baseUrl = "https://crossbrowsertesting.com/api/v3/screenshots"

	def compareSingleScreenshot(self, params):
		apiUrl = self.baseUrl + '/' + params['target_screenshot_test_id'] + '/' + params['target_version_id'] + '/' + params['target_result_id'] + '/comparison/' + params['base_result_id']
		apiUrl += '?format=json&tolerance=' + params['tolerance']
		# print(apiUrl)
		r = requests.get(apiUrl, auth=HTTPBasicAuth(self.user, self.auth))
		if r.status_code == 200:
			return r.json()['target']['comparison']['show_comparisons_public_url']
		else:
			print('Error making API call!')

	def compareFullScreenshotTest(self, params):
		apiUrl = self.baseUrl + '/' + params['target_screenshot_test_id'] + '/' + params['target_version_id'] + '/comparison/' + params['base_result_id']
		apiUrl += '?format=json&tolerance=' + params['tolerance']
		r = requests.get(apiUrl, auth=HTTPBasicAuth(self.user, self.auth))
		if r.status_code == 200:
			return r.json()['targets']
		else:
			print('Error making API call!')

	def compareScreenshotTestVersions(self, params):
		apiUrl = self.baseUrl + '/' + params['target_screenshot_test_id'] + '/' + params['target_version_id'] + '/comparison/parallel/' +params['base_version_id'] + '?format=json&tolerance=' + params['tolerance']
		r = requests.get(apiUrl, auth=HTTPBasicAuth(self.user, self.auth))
		if r.status_code == 200:
			return r.json()
		else:
			print('Error making API call')

	def getScreenshotHistory(self, params):
		apiUrl = self.baseUrl + '?format=json&num=' + params['number']
		r = requests.get(apiUrl, auth=HTTPBasicAuth(self.user, self.auth))
		if r.status_code == 200:
			return r.json()
		else:
			print('Error making API call')

user = "you@yourdomain.com"
auth = "yourauthkey"
api = CBT_Comparisons_API(user, auth)

params = {}

'''
Get comparison results for a single target screenshot result against a base screenshot result.
This is a one-to-one comparison.
'''

# params['target_screenshot_test_id'] = "12345";
# params['target_version_id'] = "12345";
# params['target_result_id'] = "12345";
# params['base_result_id'] = "12345";
# params['tolerance'] = '30'

# response = api.compareSingleScreenshot(params)
# print("URL for Single Screenshot Comparison\n" + response)

'''
Get comparison results for all browsers in target screenshot test against a base screenshot result.
The base result can be from the same test or from another test run at an earlier time. This is a
one-to-many comparison.

'''

# params['target_screenshot_test_id'] = "12345";
# params['target_version_id'] = "12345";
# params['base_result_id'] = "12345";
# params['tolerance'] = '30'

# response = api.compareFullScreenshotTest(params)
# print("URL's for Full Screenshot Comparisons:")
# for target in response:
# 	print target['comparison']['show_comparisons_public_url']

'''
Get comparison results for all browsers in target screenshot test against the same browser in the
base screenshot test. This is a good method for regression testing. For example, you've run a screenshot
test against a set of browsers that is "good". Then, after some changes, you run a new screenshot test
against the same set of browsers. This method will compare each of the same browsers against each other.
For example, IE9 will be compared to IE9 from an earlier test. This is a many-to-many comparison where
the OS/Browser/Resolution must match between the two test versions in order for the comparison to return
results. The two versions can be from the same screenshot_test_id or not.
'''

# params['target_screenshot_test_id'] = "12345";
# params['target_version_id'] = "12345";
# params['base_version_id'] = "12345";
# params['tolerance'] = '30'

# response = api.compareScreenshotTestVersions(params)

# for comparison in response:
# 	print comparison['target']['comparison']['show_comparisons_public_url']

params['number'] = '10'

response = api.getScreenshotHistory(params)
for screenshot in response['screenshots']:
	# print(screenshot)
	print('Screenshot URL + ' + screenshot['url'] + ' Screenshots Test ID: ' + str(screenshot['screenshot_test_id']))
	for version in screenshot['versions']:
		print('\tVersion ID: ' + str(version['version_id']))
		for result in version['results']:
			print('\tOS: ' + result['os']['name'] + ', Browser: ' + result['browser']['name'] + ', Result ID: ' + str(result['result_id']))
