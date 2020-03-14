+++
author = "Brian Pfeil"
categories = ["heroku"]
date = 2014-07-05T16:01:23Z
description = ""
draft = false
slug = "heroku-connect"
tags = ["heroku"]
title = "Heroku Connect"

+++


[Heroku Connect](https://www.heroku.com/connect) was announced at [Dreamforce](http://www.salesforce.com/dreamforce) '13 shortly after salesforce aquired [cloudconnect](http://www.cloudconnect.com/).  Cloudconnect is the original product created by [Adam Gross](https://twitter.com/adam_g), formerly of [Dropbox](http://dropbox.com) that became Heroku Connect.  

There's a rich developer ecosystem around web apps built with popular web frameworks such as [Rails](http://rubyonrails.org/), [Django](https://www.djangoproject.com/), [Express](http://expressjs.com/), [Symfony](http://symfony.com/), etc.  All of these frameworks assume a relational database as a backend, which because of it's age, usage, and rich set of existing toolsets, makes it easy to get started with.  Salesforce's force.com platform wanted gain this ease of use and speed at which apps could be developed.  Salesforce has it's own data storage solution that is built for scale and multitenatcy and doesn't cleanly map to the standard relational model.

Connect solves this problem by bi-directionaly synchronizing your salesforce data to a heroku postgres database.  Once in postgres, all the popular web frameworks with a huge developer community can be used to develop salesforce apps.

## Heroku Connect Setup

Connect is provided as a [heroku add-on](https://addons.heroku.com/), which enables easy intregration with heroku apps.  A prerequisite is to have a postgres database provisioned for connect to synchronize your salesforce data to.  Once your database is in place, you install the add-on via

`heroku addons:add herokuconnect -a appname`

Here's what it looks like

![](images/1.png)

The rest of the setup and configuration takes place in the Heroku Connect web interface.  You access it by logging into heroku and navigate to your app, then click the Heroku Connect link in the Add-ons section.  This will lauch the web ui.

![](images/2.png)

On first lauch you will be greeted with a setup screen.  This will automatically use to the `DATABASE_URL` config variable, which was put in place when the postgres database was provisioned.

![](images/3.png)

![](images/4.png)

The final setup looks like

![](images/5.png)

Next you need to authorize Connect to access your salesforce org

![](images/6.png)

You allow permission

![](images/7.png)

You are then ready to configure the data you want to use with Connect.

![](images/8.png)

## Resources

- [Introducing Heroku Connect: Connecting Clouds and Customers](https://blog.heroku.com/archives/2014/5/13/introducing_heroku_connect)
- [Heroku Connect Dev Center article](https://devcenter.heroku.com/articles/herokuconnect)