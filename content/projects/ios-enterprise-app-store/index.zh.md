+++
title = "iOS 企业应用商店"
description = "面向 iOS 开发者企业计划成员的内部应用分发方案。"
date = 2014-08-04T18:55:46Z
draft = false
weight = 7
+++

加入了 [iOS 开发者企业计划](http://developer.apple.com/programs/ios/enterprise/)的企业，可以通过 Apple 的[无线分发（over-the-air distribution）](http://developer.apple.com/library/ios/#featuredarticles/FA_Wireless_Enterprise_App_Distribution/Introduction/Introduction.html)，用自己的应用商店把应用分发给员工。用这套方案，你只需把应用的 .ipa 文件和一个描述该应用信息的文件放进某个目录，用户马上就能安装。

后端是一个 [Sinatra](http://www.sinatrarb.com/) Web 应用。前端内置了一套 [jQuery Mobile](http://jquerymobile.com/) 网页界面，另外还有一个独立的 iPhone 原生客户端。

**应用商店网页版**

<div>
<img style="display: inline; width: 200px;" width="200px" src="images/eas1.png"></img>
<img style="display: inline; width: 200px;" width="200px" src="images/eas3.png"></img>
</div>

**iPhone 原生客户端**

<div>
<img style="display: inline; width: 200px;" src="images/eas4.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas5.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas6.png" width="200px"></img>
</div>

*[源代码](https://github.com/pfeilbr/ios-enterprise-app-store)*
