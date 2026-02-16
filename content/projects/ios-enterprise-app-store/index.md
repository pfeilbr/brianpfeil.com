+++
title = "iOS Enterprise App Store"
description = "In-house app distribution solution for iOS Developer Enterprise Program members."
date = 2014-08-04T18:55:46Z
draft = false
weight = 7
+++

Enterprises that are members of the [iOS Developer Enterpise Program](http://developer.apple.com/programs/ios/enterprise/) can distribute their employee apps with their own App Store using Apple's [over-the-air distribution](http://developer.apple.com/library/ios/#featuredarticles/FA_Wireless_Enterprise_App_Distribution/Introduction/Introduction.html). With this solution, you just drop your app .ipa file and a file with information about the app into a directory, and it's immediately available for users to install.

The backend is a [Sinatra](http://www.sinatrarb.com/) web app. On the front-end there's a built-in [jQuery Mobile](http://jquerymobile.com/) web interface, and also a separate native iPhone app.

**App Store Web App**

<div>
<img style="display: inline; width: 200px;" width="200px" src="images/eas1.png"></img>
<img style="display: inline; width: 200px;" width="200px" src="images/eas3.png"></img>
</div>

**Native iPhone App Store Client**

<div>
<img style="display: inline; width: 200px;" src="images/eas4.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas5.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas6.png" width="200px"></img>
</div>

*[source code](https://github.com/pfeilbr/ios-enterprise-app-store)*
