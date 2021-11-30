Changelog
---------
* `1.0.1`
    * By default PDFKit handle errors from wkhtmltopdf. Now if you need to get clear output from wkhtmltopdf output, if it existed, you should pass "raise_exceptions=False" to API calls
* `1.0.0`
    * By default PDFKit now passes "quiet" option to wkhtmltopdf. Now if you need to get output you should pass "verbose=True" to API calls
    * Fix different issues with searching for wkhtmltopdf binary
    * Update error handling for wkhtmltopdf
    * Fix different issues with options handling
    * Better handling of unicode input
    * Switch from Travis to GitHub Actions
    * Update README
* `0.6.1`
    * Fix regression on python 3+ when trying to decode pdf output
* `0.6.0`
    * Support repeatable options
    * Support multiple values for some options
    * Fix some corner cases when specific argument order is required
    * Some Python 3+ compatibility fixes
    * Update README
* `0.5.0`
    * Allow passing multiple css files
    * Fix problems with external file encodings
    * Rise an error when X server is missing on \*nix systems
    * Fix tests that was broken with latest wkhtmltopdf release
    * Update README
* `0.4.1`
    * More easier custom configuration setting
    * Update README
* `0.4.0`
    * Allow passing file-like objects
    * Ability to return PDF as a string
    * Allow user specification of configuration
    * API calls now returns True on success
    * bugfixes
* `0.3.0`
    * Python 3 support
* `0.2.4`
    * Add History
    * Update setup.py
* `0.2.3`
    * Fix installing with setup.py
    * Update README
