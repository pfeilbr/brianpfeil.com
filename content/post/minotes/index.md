+++
author = "Brian Pfeil"
categories = ["ios", "app"]
date = 2013-06-21T02:43:00Z
description = ""
draft = false
slug = "minotes"
tags = ["ios", "app"]
title = "Minotes"
summary = "a clean, simple, minimal iOS notes app"

+++

<img src="images/Icon-72@2x.png" width="125px">

There are many choices for notes apps out in the App Store.  So many that it'd be a couple days effort just to look into and evaluate them all.  Everything from the built-in simple Notes app to the feature packed [Evernote](http://evernote.com/).  A notes app is one of those utility apps that gets a lot of mileage like mail and weather.  Something with high usage you want the most efficient and streamlined app.  It's also something that becomes personal and people get attached to.

I wanted something extremely simple, clean up, and fast.  I started with the simplest possible solution of a single [text view](https://developer.apple.com/library/ios/documentation/UIKit/Reference/UITextView_Class/Reference/UITextView.html) you could type in.  From that, the ability to create multiple notes was added, but I didn't want the freedom to create as many notes as you want.  Having constraints on the number of notes forces the user to create more meaningful notes and manage / clean up notes.  The goal with minotes is not to have an archive of all historical notes with search, etc.  The type of notes appropriate for this app are short-lived ones and in general have a lifespan of around a week.  I landed on a UI metaphor similar to mobile safari with a max of 9 notes.

Preferences around typography and text size is something that is really needed in order to be useful for more than a specific set of users.  For example, older people may need a little bit larger font size, whereas younger users may want to cram more text on the screen and are fine with a smaller font size.  In order to keep it simple, there are three typefaces to choose from and in sizes, small, medium, large.

It's an opinionated app built with my specific needs in mind.  It's doesn't try to appeal to all users universally, but if you like simple purpose built apps, check it out.

<div>
	<img src="images/1.png" width="150px"></img>
    <img src="images/2.png" width="150px"></img>
    <img src="images/3.png" width="150px"></img>
</div>

<a href="http://minote.net" target="_blank">Minotes Product Page</a>

<a href="https://itunes.apple.com/us/app/minotes/id648015483?ls=1&mt=8" target="_blank">
<img src="images/app-store-badge-200x100.png" width="125px">
</a>