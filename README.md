# CBT API Sample Scripts

These are sample scripts for using the CrossBrowserTesting API

## Included Script Examples:
- Live Tests: JavaScript, Python, PHP
- Screenshots: JavaScript, Python, PHP
- Comparisons: Python

[See full API documentation](https://crossbrowsertesting.com/apidocs)


## Live Tests API

Automate live tests by providing a URL and browser/operating system/device [configuration](https://crossbrowsertesting.com/). While running an automated live test, you can take a screenshot, record network packets, or record a video. Live tests started via the API will appear in the livetesting tab in the [app](https://app.crossbrowsertesting.com)

For a list of browsers compatible with the livetesting API, make a `GET` call `https://crossbrowsertesting.com/api/v3/livetests/browsers`

[Live Test API](https://crossbrowsertesting.com/apidocs/v3/livetests.html)

## Screenshots API

Automate screenshot tests by providing a URL and a list of browser/operating system/device [configurations](https://crossbrowsertesting.com/). While running a screenshot test, you can view the results in the screenshots tab in the [app](https://app.crossbrowsertesting.com).

For a list of configurations compatible with the screenshots API, make a `GET` call to `https://crossbrowsertesting.com/api/v3/screenshots/browsers`

[Screenshot Test API](https://crossbrowsertesting.com/apidocs/v3/screenshots.html)

## Screenshot Comparison API

You can compare 2 screenshots for layout differences using our screenshot layout engine. Check out the API above for more information.

[Screenshot Comparison API](https://crossbrowsertesting.com/apidocs/v3/screenshot-comparisons.html)