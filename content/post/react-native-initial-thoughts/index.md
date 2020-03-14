+++
author = "Brian Pfeil"
categories = ["javascript", "ios", "react", "react native"]
date = 2015-03-27T16:36:59Z
description = ""
draft = false
slug = "react-native-initial-thoughts"
tags = ["javascript", "ios", "react", "react native"]
title = "React Native - Initial Thoughts"

+++


![](images/react.png)

[React Native](http://facebook.github.io/react-native/) was released as open source yesterday.  There's been quite a bit of build up and excitement since the [React.js Conf 2015 video](https://www.youtube.com/watch?v=7rDsRXj9-cU).  The video showed a **real** app being built with a web development style workflow (your favorite editor with livereload).  I've built some apps using [React.js](http://facebook.github.io/react/) and really appreciate the simplicity and development workflow.  Having the same for native app development definitely is exciting.  I've gottent to spend a few hours with it and it looks like it's living up to the hype.

I started in with the [tutorial](http://facebook.github.io/react-native/docs/tutorial.html#content), which is a movies app backed by [Rotten Tomatoes](http://www.rottentomatoes.com/) data.  The main UI is a run of the mill [List View](http://facebook.github.io/react-native/docs/listview.html#content) with each cell containing a poster image, and the movie title and year.

It shows fetching data over the network, some of the concerns with rendering list views, and the react core concept of only re-rendering thing that've changes with `ListView.DataSource.rowHasChanged`.

They sprinkle in [ES6](https://github.com/lukehoban/es6features) syntax within the examples, and some of it I had to look up.  This is a good way to give people a gentle introduction to it.  I can see how it might be a bit distracting if your trying to learn something new.  Having to learn language level features on top of a new framework could be offputting for some.

## Yep. It's All in that single file.

It does a good job with starting off with a single minimal view and layering on the different concepts to get you to some more than `hello world`, but not a **real** app.  One of the things that stood out to me and made it much easier to follow is that all the code is in a single file.  UI, style, logic, and data.  This is huge from a learning and user uptake perspective.  For larger apps, it will get cumbersome quickly and using separate `.js` files and `require` them in will make it managaeble.

I've seen way too much time spent in other javascript frameworks first introducing the [file and directory layout](https://scotch.io/tutorials/angularjs-best-practices-directory-structure).  There are as many different ways to lay things out as there are javascript frameworks these days.  I agree it's important for maintainability and collaboration, but when starting out, I feel it should be kept simple, and only restructure when needed.  Choice is good, but I hope facebook explicitly documents their recommended layout and people just use it.

## Native Modules: Call for Community Contributions

If react native doesn't provide the UI component or capability you need, they allow extension via [Native Modules](http://facebook.github.io/react-native/docs/nativemodulesios.html#content).  Bridging is never pretty as it always feels like you need to switch contexts and be aware this is a `bridge component`.  They do their best to minimize this and in the spirit of react it's lightweight and only requires the minimal amount of hooks to do it's job.

You only need to implement the [RCTBridgeModule](http://facebook.github.io/react-native/docs/nativemodulesios.html#ios-calendar-module-example) [protocol](https://developer.apple.com/library/ios/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/WorkingwithProtocols/WorkingwithProtocols.html) to expose native code.

Here's the [example](http://facebook.github.io/react-native/docs/nativemodulesios.html#content)

```
// CalendarManager.h
#import "RCTBridgeModule.h"

@interface CalendarManager : NSObject <RCTBridgeModule>
@end

// CalendarManager.m
@implementation CalendarManager

- (void)addEventWithName:(NSString *)name location:(NSString *)location
{
  RCT_EXPORT();
  RCTLogInfo(@"Pretending to create an event %@ at %@", name, location);
}

@end

var CalendarManager = require('NativeModules').CalendarManager;
CalendarManager.addEventWithName('Birthday Party', '4 Privet Drive, Surrey');
```

As you can see, it's minimally intrusive on both the objc and js sides.

Native Modules is the community aspect of this effort and if done right will give it staying power.  The productivity and developer workflow benefits of `npm install awesomesauce` is the one of the core underlying reasons for javascript/node popularity.

A decision needs to be made on whether [npm](https://www.npmjs.com/) or a native packager like [Cocoapods](http://cocoapods.org/) will be the vehicle for packaging and distributing native modules.  To keep it x-platform and support android, npm would be the obvious choice.  It's important for the react native team to make a decision on this and define this from the start.  People will fill the gaps that react native doesn't include. The easier you make it for them to publish for community, the better off the ecosystem will be.

## [Fetch](https://fetch.spec.whatwg.org/)

Networking and more specifically the ability to fetch HTTP resources is a core capability of a majority of applications today.  While walking through the tutorial I saw the use of [fetch](http://facebook.github.io/react-native/docs/network.html#content), but had never seen it before.  I thought it was something that facebook defined and injected that bridged into iOS's networking.  It does this, but in addition it's based on the [fetch networking API](https://fetch.spec.whatwg.org/), which is going through the standard process.  Hopefully a higher profile project like react native will give it some legs.


## Onward

Native development on the native target platform will always be more popular.  It doesn't strive to or need to try to supplant native development.  Capturing the web development community alone is a huge audience.  More importantly, the react community is full of super star developers that will acively champion things they like.  If it reached the success of a [Xamarin](http://xamarin.com/) and as large a community, it would be quite an achievement.

It's early and if you don't have a lot free time or care to be on the bleeding edge, I'd recommend waiting a bit before using it to develop a production app.  As with anything new and in interest of the long-term goals, I'm sure there will be bugs to work through, breaking changes, API changes, additional development and debugging tooling, etc.

Even if I don't dive right in, at a minimum I'll keep up with it's progress via rss feeds and twitter.  Kudos to the react native team for a great launch and wish them the best.