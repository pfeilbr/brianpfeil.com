+++
author = "Brian Pfeil"
categories = ["web", "heroku"]
date = 2012-09-16T02:43:00Z
description = ""
draft = false
slug = "hosting-static-sites-on-heroku"
tags = ["web", "heroku"]
title = "Hosting Static Sites on Heroku"

+++



<img src="/assets/heroku.jpg" width="125px">

I was recently creating a web site for a family member, and was looking around for the best place to host it.  It's a simple personal site that only contains static content.  There are many options out there from the freebie wordpress options to rackspace and the like.  None of the "web publishing platform" type sites were a fit because I wanted full control over the layout, and look and feel of the site.

I've been working with [Heroku](http://heroku.com) for my day job for web applications, and it's been simple to get things up and running at no cost.  Heroku allows you to create a web application for free, and only if you need to scale to support the traffic do you have to pay.

One of the limitations of using the free plan with heroku is that if your app hasn't recieved any traffic within an hour, it puts it into an idle state.  They call this [dyno idling](https://devcenter.heroku.com/articles/dynos)  and when a request comes in and your dyno is in an idle state, it has to spin it back up, and that takes time.  In my experience, I'll go to hit the site and it takes approx. 5 seconds to respond.  It's free, so I can understand when they do this to save on compute resources, and if you have pay / have multiple dynos, they never with idle your app.

To work around this you just need to have at least 1 request come in an hour.  There are many ways to do this, and I took the simple approach of using a monitoring service ([pingdom](https://www.pingdom.com/)) to check/ping the site for availability every 5 minutes.  You could also implement by using a background worker process.


There’s a great [Creating Static Sites in Ruby with Rack](https://devcenter.heroku.com/articles/static-sites-ruby) walkthrough on the heroku dev center that will have you up and running in few minutes. They provide a fully functional [sample application](https://github.com/leereilly/static-site-heroku-cedar-example) that you can modify to make you own.