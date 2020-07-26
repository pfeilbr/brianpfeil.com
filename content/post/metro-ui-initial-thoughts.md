+++
author = "Brian Pfeil"
categories = ["windows", "win8", "metro"]
date = 2011-09-21T23:12:00Z
description = ""
draft = false
slug = "metro-ui-initial-thoughts"
tags = ["windows", "win8", "metro"]
title = "Metro UI: Initial Thoughts"
summary = "slick new UI overhaul for Windows"

+++



I've been digesting all the new information around Windows 8 and Metro over
the past week. I've watched the [BUILD Conference](http://www.buildwindows.com/) [Channel 9 Videos](http://channel9.msdn.com/Events/BUILD/BUILD2011?t=metro%2Bstyle%2Bapp),
read the articles and docs on the [Windows Dev Center](http://msdn.microsoft.com/en-us/windows/apps/) and the [Building Windows 8 blog](http://blogs.msdn.com/b/b8/). The best resource for your time
on learning what Metro is all about from a design perspective is [8 traits of great Metro style apps](http://channel9.msdn.com/Events/BUILD/BUILD2011/BPS-1004).

The Metro Style interface is a totally new and original approach to UI.
Microsoft put a lot of thought into the design of it, and they demonstrated
this by providing background during the BUILD sessions on how they studied how
users held and used slate devices, what areas of the screen where reachable by
their thumbs, etc.

The concept of dedicating all the available screen space to content with no
chrome makes perfect sense. It doesn't makes sense for all applications,
especially those rich in functionality. For example, Microsoft showed
Photoshop and it's many tool palettes and menus, and it was clear that you
wouldn't make a Metro Style Photoshop app. Metro makes sense for "consumery"
type apps like casual games, productivity apps, and rich media apps; the same
things you see on an iPad or Android tablet. This is one of the reasons that
they need to support "classic" windows app, and they can't make a clean break
to the Metro Style UI.

One potential problem with the immersive content, and no chrome approach is
the lack of discoverability to take actions on the content. Metro relies
heavily on gestures that take place at the edges of the screen. For example to
display the charm bar, you place your finger off to the right of the screen
where there isn't any content and touch isn't recognized then swipe in towards
the center of the screen. Another example is the application bar at the bottom
where you have to swipe up to summon it. Is a user gonna know to do this? Will
devices come with an in-your-face tutorial on these things when you first boot
it up?  There have been many studies that have proven if it's out of site then
users won't discover it. For touch, there are only two gestures you should
assume your users know, and that's tap and swipe to scroll; everything else is
power user territory.

There's another issue around using a mouse in Metro. Microsoft made the
statement that Metro is a natural fit for a mouse in addition to touch. I've
been using the Developer Preview running in VMware, and using a mouse with
Metro is very tedious. The level of indirection you have between the mouse and
what happens on the screen makes the things that work well with touch feel
like a large amount of effort. I actually resorted to using the [windows 8 keyboard shortcuts](http://www.groovypost.com/groovytip/windows-8-metro-keyboard-shortcuts/).
to activate the standard toolbars and menus because it was so painful. If the
apps interaction is limited to clicks and/or keyboard input with no
application bar, then the mouse could work, but that's only gonna be a handful
of apps.

The tiles interface for the home screen was very visually appealing in all the
BUILD demos with nice typography, rich pictures, and pastel colors. This is
great and demos well when Microsoft controls all the apps, but what happens
when you have a whole community of app developers who have their own opinions
on design and style building Metro apps. The app that doesn't use a pastel
color for their tile background, shows a poorly shot overexposed photo that
the user took on their phone, uses an ugly icon, etc. There's nothing from
keeping people from doing this. Microsoft is aware of this and they emphasized
many times in the BUILD sessions to use the templates they provide in Visual
Studio 11. This is a problem on any platform, and it happens on iOS and
Android, but the reason it's a bigger issue for Metro is that it's critical to
have in place for the immersive experience. All you have is content. You don't
have standard chrome title bars and toolbars with a standard look and feel to
make your app fit in. Content is everything, and if it's poor, then it'll
stick out like a sore thumb.

It's still early. Microsoft always previews things and gets them out early to
users, so I'm sure there'll be some tweaks. This is a big change for them, and
the most recent thing as big as this has been there move into the game console
space with XBox. Time will tell.


