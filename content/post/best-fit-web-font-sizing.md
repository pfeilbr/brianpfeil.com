+++
author = "Brian Pfeil"
categories = ["html", "javascript", "fonts"]
date = 2011-09-27T19:31:00Z
description = ""
draft = false
slug = "best-fit-web-font-sizing"
tags = ["html", "javascript", "fonts"]
title = "Best Fit Web Font Sizing"
summary = "dynamically size web font based on available space"

+++



I've been working on a web app that targets both smartphones and tablets. The
large variation in screen sizes has sent me down the path of using a dynamic
proportional layout that adapts to fit the available space. For example, I've
allocated 20% of the available vertical space to the header section that
displays a title. The [jQuery UI.Layout Plug-in](http://layout.jquery-dev.net/) has worked great for laying out the
content areas, but I ran into a wall when it came to sizing my text
proportionately.

The basic problem is that I have a box, and I want to display some text in it
at the largest font size without it being wrapped or clipped. The only way to
determine the bounding rectangle a string of text with certain font
characteristics, is to create it, add it to the DOM, and then measure it. The
following function does just that.

```language-javascript
function sizeWithText(text, cssStyles) {
	// create temp element to hold our text
	var e = document.createElement('span');
	e.appendChild(document.createTextNode(text));

	// apply any styles that have been passed in
	// to our element - these can affect the text size
	for (var prop in cssStyles) {
		e.style[prop] = cssStyles[prop];
	}

	// hide our temp element
	e.style['visibility'] = 'hidden';

	// add to DOM in order to have it render
	document.body.appendChild(e);

	// get the bounding rectangle dimensions
	var s = {w: e.offsetWidth, h: e.offsetHeight};

	// remove from DOM
	document.body.removeChild(e);

	return s;
}
```

The `cssStyles` parameter holds the other css style attributes that you'd like to apply to the text.  For example, you might have a `font-weight: bold` attribute that increases the size of the text, and we want to make sure we account for it.

Now we can use this function to check whether text with a font size and a set of styles will fit in our box.  We set the font size to 1 and continuously increase it by 1 check whether it'll fit at every iteration.  As soon as it doesn't, we stop.

```language-javascript
function bestFitTextSize(text, css, width, height) {
	var pixel = 1;

	do {
		css['font-size'] = (pixel++) + 'px';
		s = sizeWithText(text, css);
	} while ( (s.w < width) && (s.h < height) )

	return pixel - 2;
}
```

This is a brute force and inefficient way to do the calculation, and there are improvements that could be made.  We could start at a reasonable font size like 6px, increment by standard font sizes, etc., but this is fine for my usage where I only do it once on app load.

Here's a code sample that shows how the previous functions are used.

```language-javascript
// box we want to fill with text
var c = document.getElementById('content');

// out text
var text = 'Lorem ipsum dolor sit amet';

// styles
var cssStyles = {
	'font-family': 'Impact',
	'font-style': 'normal',
	'font-weight': 'bolder',
	'letter-spacing': '1px',
	'text-shadow': '3px 3px 3px white'
};

// size the text to fit
function applyBestFitText() {
	// get the pixel size for the font
	var px = bestFitTextSize(text, cssStyles, c.offsetWidth, c.offsetHeight);
	cssStyles['font-size'] = px + 'px';

	// set the text
	c.innerHTML = text;

	// apply our styles
	for (var prop in cssStyles) {
		c.style[prop] = cssStyles[prop];
	}
}

// adjust if the size changes
window.addEventListener('resize', applyBestFitText, false);

// call for first time adjustment
applyBestFitText();

```

The complete example is available as a [gist](https://gist.github.com/1248669)