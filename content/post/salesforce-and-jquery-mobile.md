+++
author = "Brian Pfeil"
categories = ["salesforce", "jquery", "mobile"]
date = 2011-09-11T00:58:00Z
description = ""
draft = false
slug = "salesforce-and-jquery-mobile"
tags = ["salesforce", "jquery", "mobile"]
title = "Salesforce and jQuery Mobile"

+++



I wanted to do a project to learn [salesforce], but not a trivial hello
world style example. I had recently played around with [jQuery Mobile], but
didn't do anything significant with it. I decided to put together a basic
mobile CRM app.  Here's what the finished app looks like.

![contact list screen shot](https://img.skitch.com/20110910-enbnxextqtsfyc431skq2m9ws6.png)
![view contact screen shot](https://img.skitch.com/20110910-di6tn8haxrr7abtks1927cj11r.png)
![edit contact screen shot](https://img.skitch.com/20110910-mq92tg5csrc43equ7rskyyjrp1.png)

[Salesforce] provides a full-featured environment for free to anyone. It takes
no time to [sign-up] for this [Developer Edition], and you get access to
everything. If you're just getting started with [salesforce], I *can't
recommend enough* the online tutorials, workbooks, and documentation at
[developer.force.com].

## Accessing the App Data ##

Our app will contain Contact and Account data.  We'll use Apex Web Service methods to provide the data.  We can get all our Contacts with the following:

```java
webService static List<Contact> getContacts() {
	ApexPages.StandardSetController setCon = new ApexPages.StandardSetController(
		Database.getQueryLocator(
        	[select id, name, lastname, firstname, title, department, phone, email from Contact]));
    return (List<Contact>)setCon.getRecords();
}
```

Next we need to call the web service method from the client code.  We'll use the force.com ajax apex javascript libraries to access our data.  Add these script references to your page `<head>` section.

```html
<script src="/soap/ajax/15.0/connection.js"></script>
<script src="/soap/ajax/15.0/apex.js"></script>
```

To call the web service method from JavaScript we use this simple one-liner.

```js
var contacts = sforce.apex.execute("MyWebService", "getContacts", {});
```

## Building the UI ##

Our mobile app UI will be 100% [jQuery Mobile], and we can use [force.com]
[Sites] to provide pure web content. [Sites] by default provides configurable
headers, footers, navigation, etc. that you can apply themes to. We don't want
any of this in our app since we'll be controlling everything in the UI. To
turn off the default stylesheets, header, and navigation elements your
`apex:page` element should set the corresponding attributes, and should look
similar to the following:

```html
<apex:page showHeader="false" sidebar="false" standardStylesheets="false" contentType="text/html">
```

Now we'll add in the jQuery Mobile references.

```html
<link rel="stylesheet" href="http://code.jquery.com/mobile/1.0b2/jquery.mobile-1.0b2.min.css" />
<script src="http://code.jquery.com/jquery-1.6.2.min.js"></script>
<script src="http://code.jquery.com/mobile/1.0b2/jquery.mobile-1.0b2.min.js"></script>
```

The beauty of jQuery Mobile is that all you have to do is markup your html
with the correct attributes to get a mobile UI. You don't need to write any
JavaScript. Usually you serve up the jQuery _Mobilized_ html from the server.
We want our app to run and function when the device is offline, so we're going
to generate the html at run-time on the client using JavaScript to remove the
dependency on the server.

To minimize the amount of html we embed in our JavaScript, we're going to use
[jQuery Templates]. [jQuery Templates] allows us to write our html for the UI
as we usually would, and to leave placeholders for the pieces we want to
replace. Here's an example of a template used to generate a list page.

```html
<script id="object-list-page-template" type="text/x-jquery-tmpl">

<div data-role="page" id="${type}-list-page" data-url='${type}-list-page'>
	<div data-role="header">
		<h1>${pageTitle}</h1>
		<a id='${type}-add-link' data-obj-type='${type}' class='ui-btn-right object-add-link' data-icon="add">Add</a>
	</div>

	<div data-role="content">
		<ul data-role="listview" id="${type}-list" data-filter="true">
		</ul>
	</div>

	<div data-role="footer" data-id='footer-nav-bar' data-position="fixed">
		<div data-role="navbar">
			<ul>
				<li><a href="#contact-list-page" data-transition="fade" class="${(type == 'contact') ? 'ui-btn-active' : ''} ui-state-persist">Contacts</a></li>
				<li><a href="#account-list-page" data-transition="fade" class="${(type == 'account') ? 'ui-btn-active' : ''} ui-state-persist">Accounts</a></li>
			</ul>
		</div>
	</div>
</div>

</script>
```

The things wrapped in `${}` are replaced with the values.  The way we use the template is by calling the `$.tmpl` method.

```js
var $page = $('#object-list-page-template').tmpl(data);
```

jQuery Templates are very powerful, and really help with the maintainability of your code.  Check out the [documentation](http://api.jquery.com/jQuery.template/) to learn more.

## Conclusion ##

This provides an overview of the core pieces of the solution and the technologies used.  If you like to dive in deeper, the complete source is available on **[github](https://github.com/pfeilbr/salesforce-jquery-mobile)**, and the working app is available **[here](http://j.mp/msales-dev)** (must be viewed in a [WebKit] based browser).

[force.com]: http://force.com
[salesforce]: http://salesforce.com
[developer.force.com]: http://developer.force.com
[Developer Edition]: http://wiki.developerforce.com/index.php/Developer_Edition
[sign-up]: http://www.developerforce.com/events/regular/registration.php
[Sites]: http://developer.force.com/sites
[jQuery Mobile]: http://jquerymobile.com/
[jQuery Templates]: http://api.jquery.com/jQuery.template/
[WebKit]: http://www.webkit.org/