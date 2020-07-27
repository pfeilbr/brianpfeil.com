+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2015-02-15
description = ""
summary = "learning Karma"
draft = false
slug = "karma"
tags = ["github",]
title = "Karma"
repoFullName = "pfeilbr/karma-playground"
repoHTMLURL = "https://github.com/pfeilbr/karma-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/karma-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/karma-playground</a>
-->


Project to learn and experiment with the Karma javascript test runner.  Karma runs your javascript tests in multiple browsers.


## Quickstart Tutorial

1. Change to project directory

		$ cd ~/projects/karma-playground

2. New NPM project
	
		$ npm init

	> *accept all defaults*

3. Install karma

	```bash
	# Install Karma:
	$ npm install karma --save-dev

	# Install plugins that your project needs:
	$ npm install karma-jasmine karma-chrome-launcher --save-dev
	```

4. Install global karma cli so we can type `karma` without the full path from anywhere.

		$ npm install -g karma-cli


5. Create sample test.

	> Using [Jasmine](http://jasmine.github.io/) for our example.

	```bash
	$ mkdir test
	$ touch test/sample1.js
	```
	
	```js
	// test/sample1.js
	describe("A suite", function() {
	  it("contains spec with an expectation", function() {
	    expect(true).toBe(true);
	  });
	});
	```

6. Generate the karma configuration file 

		$ karma init my.conf.js


7. Start karma

		# Start Karma using your configuration:
		$ karma start my.conf.js

	> You'll see Chrome or the browsers you chose start

![](http://note.io/1FdGfLE)


