+++
author = "Brian Pfeil"
categories = ["salesforce", "mobile"]
date = 2013-12-11T22:11:00Z
description = ""
draft = true
slug = "getting-started-with-salesforce-mobile-push-notification-service"
tags = ["salesforce", "mobile"]
title = "Getting Started with Salesforce Mobile Push Notification Service"
summary = "Salesforce introduced the Mobile push notifications Developer Preview with Dreamforce 13"

+++



Salesforce introduced the Mobile push notifications Developer Preview with Dreamforce 13.  It's available by default in all new Developer Edition organizations created after November 7, 2013.

* create new DE org
* create connected app
	* add APNS cert
* create native iOS app from iOS Mobile SDK
* create apex code to send push notification

# Outline

* link to salesforcemobilepushnotificationservice.pdf doc [](http://downloads.salesforce.com/salesforce_mobile_push_notification_service.pdf)
* forceios create
	* npm install [forceios](https://npmjs.org/package/forceios)
* consumer key and callback screenshot mapping from setup UI to iOS code
* uncommenting code in iOS Mobile SDK template
* apex code
* pass in optional apex page URL to navigate to on Notification launch in APS payload
	* launch apex page via frontdoor.jsp
* link to [APNS payload spec from Apple](https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/ApplePushService.html#//apple_ref/doc/uid/TP40008194-CH100-SW1)
* sample Notifier app
* link to DF presentation and video with @mention of Kevin Harris @imsorrysandwich
	* session name "Adding Notifications to Your Mobile App With the Universal Notification Service"