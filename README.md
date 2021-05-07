# algorhythm-use-case

*Note: this project isn't in a working state, but had to be delivered as is because of time constraints.*

This repository contains files to create a Flask app to summarize a book of the [Project Gutenberg website](https://gutenberg.org/).

As mentioned in the note above, the app doesn't function yet. The front end website and the back end python script are not connected yet because of several performance issues and bugs.

The idea was that the user visiting the site should provide the url to the book to summarize, and click the Submit button. Then the url would be passed to the python script to:
* fetch the text
* clean it
* preprocess it to pass it to a model
* summarize the text
* return the result

The python script can be found in the tools directory.