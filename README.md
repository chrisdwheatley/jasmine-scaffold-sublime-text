# Jasmine Scaffold

A Sublime Text 3 plugin to help scaffold out your Jasmine tests without any JS.

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
	* `CMD + ALT + SHIFT + J` for OSX users
	* `CTRL + ALT + SHIFT + J` for Windows & Linux users
	* Right click the file and click `Run Jasmine Scaffold`

Your specification will immediately be formatted as required by Jasmine ready for tests to be added.

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