# Jasmine Scaffold

A Sublime Text plugin to help scaffold out your [Jasmine](https://github.com/jasmine/jasmine) tests without the JS.

### Usage

* Write your specifications in plain English, indenting where required. e.g.

```
a unit of code
	when correctly initialised
		should run the desired functionality
	when incorrectly initialised
		should return the correct error
```

* Run Jasmine Scaffold:
	* <kbd>Cmd</kbd> <kbd>Alt</kbd> <kbd>Shift</kbd> + <kbd>J</kbd> for OSX users
	* <kbd>Ctrl</kbd> <kbd>Alt</kbd> <kbd>Shift</kbd> + <kbd>J</kbd> for Windows & Linux users
	or
	* Right click within the file editor area and click 'Run Jasmine Scaffold'

Your specification will immediately be formatted into JavaScript code ready for tests to be added. e.g.

```javascript
describe('a unit of code', function() {

	describe('when correctly initialised', function() {

		it('should run the desired functionality', function() {

		});

	});

	describe('when incorrectly initialised', function() {

		it('should return the correct error', function() {

		});

	});

});

```

### License

Released under the MIT license: [opensource.org/licenses/MIT](http://opensource.org/licenses/MIT)
