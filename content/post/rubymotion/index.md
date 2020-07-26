+++
author = "Brian Pfeil"
categories = ["ruby"]
date = 2012-05-11T01:34:00Z
description = ""
draft = false
slug = "rubymotion"
tags = ["ruby"]
title = "RubyMotion"
summary = "leverage your Ruby skills to build native iOS apps"

+++



![RubyMotion](images/ruby-motion.png)

[RubyMotion](http://www.rubymotion.com/) is a toolchain that lets you develop
iOS using [Ruby](http://www.ruby-lang.org/). I'm a big fan of Ruby and have
been using it on and off since 2001. It's been a huge timesaver in many cases
allowing me to quickly script solutions. When I heard it was coming to iOS I
had to check it out.

The toolchain and the way you use the various components matches the
[rails](http://rubyonrails.org/) development process. Open your favorite text
editor and a terminal, and you're ready to go. For example to create a new
project.

``` sh
motion create project
```

Interfacing with the toolchain is all [rake](http://rake.rubyforge.org/)
driven. Edit your files, type `rake device`, and your app is compiled and
launches in the iOS Simulator. It's a very nice and familiar development
process.

One of the big benefits with using Ruby is concise code. Compared to
[Objective-C](http://en.wikipedia.org/wiki/Objective-C), you'll end up with a
lot less code for an app. For example with Ruby, you could put your entire app
in a single .rb file. With Objective-C you have the .h and .m files for every
class, and you spend quite a bit of time switching between them all.

Ruby helps ease the app development process, but most of the learning and
skill with iOS development is understanding the various iOS frameworks. This
doesn't go away with RubyMotion. You still have to take the time to learn
these. Part of learning is reviewing the code samples that Apple provides, and
they're all in Objective-C. Knowing the native language of a platform is
always the best thing, and if someone wanted to get started with iOS
development, I'd recommend learning Objective-C.

RubyMotion costs $200, and this might be a barrier for it taking off. The Ruby
community is used to things being open source and **free**. It'd be nice if
they took the approach Apple does with Xcode. With a free Apple Developer
account, you can create apps, but your limited to running them in the
simulator. Once you pay the $99 for to be a part of the developer program, you
can put apps on devices and the App Store. RubyMotion could do the same, free
for apps running on the simulator, and purchase to put apps in the App Store.

The creator of it is former Apple employee, [Laurent
Sansonetti](http://twitter.com/lrz), who also led the development of the
[MacRuby](http://www.macruby.org/) project, which tries to achieve the same
goal by allowing devs to create OS X apps with Ruby. Apple supported the
MacRuby project heavily in the past, but it seems to have slowed with the rise
of iOS. I have to think that Sansonetti proposed Ruby on iOS while he was at
Apple, but it didn't get support internally. Apple doesn't like platforms
being built on top of it's own platforms because they loose control and if the
apps created using the platform don't match the user experience Apple wants,
they can't do anything about it (remember flash).

I'm skeptical that it'll take off, but am definitely rooting for it.