### Sublime PythOnSelection

## About
A Sublime Text 3 plugin that executes Python code on the selected text.

This plugin provides two commands: 'Eval on each selection' and 'Format each selection'. The first one executes Python code on the current selection, while the second outputs the result of the given string formatting syntax.

## Installing
The easiest way to install PythOnSelection is through Package Control, which can be found at this site: [http://wbond.net/sublime_packages/package_control](http://wbond.net/sublime_packages/package_control)

## Code execution

The 'Eval on each selection' command asks the user to input a single line Python expression that is executed on the current seletion (or on each selection in case of multiple carets). The code can access the following variables:

* `v` is the value of the selection
* `i` is the index of the selection (`0` in case of single selection)
* `si` is the index value converted to string
* `l` is the number of characters of the current selection
* `sl` is the number of characters of the current selection converted to string
* `_` is a shortcut to a space character (i.e. `" "`)
* `f` is a function that called on a string as `f(somestring)` executes `somestring.format(**vars)` where `vars` are all the above variables.

You have also access to some preimported modules, `string`, `math`, and `re`.

## Format

The 'Format each selection' command asks the user to input a formatted string with the syntax used by the Python `format()` string method. The given string is then formatted with the following variables:

* `v` is the value of the selection
* `i` is the index of the selection (`0` in case of single selection)
* `l` is the number of characters of the current selection

## Code execution examples

* **Uppercase**: select some text and execute `v.upper()`
* **Title**: select some text and execute `v.title()`
* **0-indexed list**: select the beginning of some lines (multiple caret) and execute `si + _`
* **1-indexed list**: select the beginning of some lines (multiple caret) and execute `str(i + 1) + _`
* **Replace punctuation with space**: select some text and execute `v.translate({ord(k):_ for k in string.punctuation})`
* **Regular expressions**: select some text and execute `re.sub(r'_', ' ', v)`

## Format examples

* **0-indexed list**: select the beginning of some lines (multiple caret) and execute `{i} `
* **Put a left-aligned index (up to 99)**: select the beginning of some lines (multiple caret) and execute `{i:>2} `
