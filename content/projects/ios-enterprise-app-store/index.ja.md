+++
title = "iOS 社内アプリストア"
description = "iOS Developer Enterprise Program 参加企業のための社内アプリ配布の仕組み。"
date = 2014-08-04T18:55:46Z
draft = false
weight = 7
+++

[iOS Developer Enterprise Program](http://developer.apple.com/programs/ios/enterprise/) に参加している企業は、Apple の[無線配信（over-the-air distribution）](http://developer.apple.com/library/ios/#featuredarticles/FA_Wireless_Enterprise_App_Distribution/Introduction/Introduction.html)を使って、自前のアプリストアから社員向けアプリを配布できます。この仕組みでは、アプリの .ipa ファイルとアプリの情報を書いたファイルをディレクトリに置くだけで、すぐにユーザーがインストールできる状態になります。

バックエンドは [Sinatra](http://www.sinatrarb.com/) の Web アプリです。フロントエンドには [jQuery Mobile](http://jquerymobile.com/) の Web インターフェースが組み込まれているほか、別途 iPhone のネイティブアプリもあります。

**アプリストアの Web 版**

<div>
<img style="display: inline; width: 200px;" width="200px" src="images/eas1.png"></img>
<img style="display: inline; width: 200px;" width="200px" src="images/eas3.png"></img>
</div>

**iPhone ネイティブのアプリストアクライアント**

<div>
<img style="display: inline; width: 200px;" src="images/eas4.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas5.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas6.png" width="200px"></img>
</div>

*[ソースコード](https://github.com/pfeilbr/ios-enterprise-app-store)*
