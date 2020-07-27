+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2015-10-15
description = ""
summary = "learning Cordova"
draft = false
slug = "cordova"
tags = ["github",]
title = "Cordova"
repoFullName = "pfeilbr/cordova-playground"
repoHTMLURL = "https://github.com/pfeilbr/cordova-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/cordova-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/cordova-playground</a>


Project to learn and experiment with [Apache Cordova](https://cordova.apache.org/)

## Running

1. Clone this repo
2. Run the following

  ```sh
  $ cd cordova-playground
  $ cordova prepare
  $ cordova build ios
  $ cordova emulate ios
  ```

## Leveraging [JSforce](https://jsforce.github.io/)

To ensure the salesforce [JSforce](https://jsforce.github.io/) javascript library can make `https://*.salesforce.com` requests from `file:///`.

1. The following must be added to `config.xml`

  ```xml
    <access origin="*" />
  ```

2. For iOS 9 and above, apple introduced [App Transport Security](https://blog.nraboy.com/2015/10/fix-ios-9-app-transport-security-issues-in-apache-cordova/).  It can be fixed by adding the following to `Info.plist`

  ```xml
  <key>NSAppTransportSecurity</key>  
  <dict>  
      <key>NSAllowsArbitraryLoads</key>
      <true />  
  </dict>
  ```

3. Add `www/js/jsforce.js` and add a `<script>` for it in `www/index.html`.

4. Needed to comment out the following in `index.html`

  ```html
  <!--
  <meta http-equiv="Content-Security-Policy" content="default-src 'self' data: gap: https://ssl.gstatic.com 'unsafe-eval'; style-src 'self' 'unsafe-inline'; media-src *">
  -->
  ``` 

5. Run the following to rebuild and show in simulator

  ```sh
  $ cordova prepare
  $ cordova build ios
  $ cordova emulate ios
  ```

---

**Sample javascript used to test**

```javascript
var conn = new jsforce.Connection({loginUrl : 'https://test.salesforce.com'});
conn.login('brian.pfeil@merck.com.hhusd11', '<PASSWORD>', function(err, res) {
  if (err) { return console.error(err); }
  conn.query('SELECT Id, Name FROM Account limit 1', function(err, res) {
    if (err) { return console.error(err); }
    alert(JSON.stringify(res));
  });
});
```

---

**Safari Web Inspector Session Screenshot**

![](http://static-content-01.s3-website-us-east-1.amazonaws.com//iPhone_6s_Plus_-_iPhone_6s_Plus___iOS_9_0__13A340__1BD012AC.png)

## Key Files

```
config.xml
www/index.html
www/js/index.js
```

## Resources

* [Cordova | iOS Whitelisting](https://cordova.apache.org/docs/en/3.6.0/guide/appdev/whitelist/index.html#link-4)
* [Christophe Coenraets | Apache Cordova Tutorial](https://ccoenraets.github.io/cordova-tutorial/index.html)
* [Fix iOS 9 App Transport Security Issues In Apache Cordova](https://blog.nraboy.com/2015/10/fix-ios-9-app-transport-security-issues-in-apache-cordova/)


