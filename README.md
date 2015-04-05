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

* Run Jasmine Scaffold (you can run for the whole file or highlight a selection of your file and run only for that):
	* <kbd>Ctrl</kbd> <kbd>Cmd</kbd> <kbd>Shift</kbd> + <kbd>J</kbd> for OSX users
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

### Contributing

Contributions are more than welcome, no matter how large or small. The workflow I used for working on the plugin as follows (YMMV):

* On your command line navigate to the packages folder for Sublime Text, which by default for Sublime Text 3 is located at `Users\”Username”\Library\Application Support\Sublime Text 3\Packages` on OSX and
`C:\Users\”Username”\AppData\Roaming\Sublime Text 3\Packages` on Windows.

* Fork the project within GitHub.

* Clone your fork & `cd` into it

```
git clone git@github.com:"Username"/jasmine-scaffold-sublime-text.git & cd jasmine-scaffold-sublime-text
```

You'll then be able to test the plugin as you make changes directly in Sublime Text. There are sample files to test on within the `test` directory.

Commit your work, push it to GitHub and submit a pull request with an explanation of the patch.

### License

Released under the MIT license: [opensource.org/licenses/MIT](http://opensource.org/licenses/MIT)
