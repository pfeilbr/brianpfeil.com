+++
author = "Brian Pfeil"
categories = ["mac", "network"]
date = 2011-08-05T00:58:00Z
description = ""
draft = false
slug = "automatic-network-location"
tags = ["mac", "network"]
title = "Automatic Network Location"

+++



I bounce back and forth between work and home with a MacBook Pro.
At work, I'm behind a firewall, and have to go through a web proxy to get to
public internet sites. I have 2 network locations setup, **home** and **work**.  When
I get to work I manually set my location to work, and when I get home, I
manually set it to home again.

![setting network location](https://img.skitch.com/20110805-8q2h4g192xqa96xf4tfh6g1gcc.png)

I got tired of remembering to do this so I looked around, and found [scselect][].
`scselect` is a command line utility that comes with
**OS X** that lets you set your location by name

{% codeblock file.sh %}
scselect "home"
{% endcodeblock %}

Now all I needed was a way to determine whether I was at work or home and then run
[scselect][] with the corresponding location.  My work assigned ip address has a
set prefix, so I can use that to say I'm at work and anything else would default
to home.

{% codeblock file.sh %}
# exit code is 0 if on work network and 1 otherwise
ifconfig | grep -i "inet 59.33" > /dev/null
{% endcodeblock %}

In order to prevent setting the location to the same location we need to find out
what the current location is.  Running `scselect` with no arguments displays a list
of locations and the active one is marked with an asterisk (*).  Here's my list.

{% codeblock file.sh %}

> scselect
Defined sets include: (* == current set)
   575844ED-8466-479C-9567-3F0B7D767EE9	(home)
   3DF4B8B9-2E92-4F61-B684-74E0D0D38DEE	(Automatic)
 * 6064213B-532D-43C9-8941-DC72B6487955	(work)

{% endcodeblock %}

The output is a bit messy, and we need to parse out the active location.

{% codeblock file.rb %}
#!/usr/bin/env ruby

# example output: * 6064213B-532D-43C9-8941-DC72B6487955	(work)
output = `scselect 2>&amp;1 | grep ' \\* '`

# parse out the location.
location = output.scan(/\(.*\)/).first.gsub(/[\(\)]/, "")

# location = work
{% endcodeblock %}

We now compare the active location with the location our ip address tells us.  If different,
we call `scselect` with the new location.

Complete script is available [here](https://gist.github.com/1195922)

[scselect]: http://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man8/scselect.8.html