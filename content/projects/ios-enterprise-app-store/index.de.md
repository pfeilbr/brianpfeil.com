+++
title = "iOS Enterprise App Store"
description = "Lösung zur internen App-Verteilung für Mitglieder des iOS Developer Enterprise Program."
date = 2014-08-04T18:55:46Z
draft = false
weight = 7
+++

Unternehmen, die am [iOS Developer Enterpise Program](http://developer.apple.com/programs/ios/enterprise/) teilnehmen, können ihre Mitarbeiter-Apps über einen eigenen App Store verteilen — per [Over-the-Air-Distribution](http://developer.apple.com/library/ios/#featuredarticles/FA_Wireless_Enterprise_App_Distribution/Introduction/Introduction.html) von Apple. Mit dieser Lösung legt man einfach die .ipa-Datei der App zusammen mit einer Datei mit den App-Informationen in ein Verzeichnis, und schon steht sie zur Installation bereit.

Das Backend ist eine [Sinatra](http://www.sinatrarb.com/)-Web-App. Im Frontend gibt es eine eingebaute Weboberfläche auf Basis von [jQuery Mobile](http://jquerymobile.com/) sowie zusätzlich eine native iPhone-App.

**App-Store-Web-App**

<div>
<img style="display: inline; width: 200px;" width="200px" src="images/eas1.png"></img>
<img style="display: inline; width: 200px;" width="200px" src="images/eas3.png"></img>
</div>

**Nativer iPhone-Client für den App Store**

<div>
<img style="display: inline; width: 200px;" src="images/eas4.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas5.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas6.png" width="200px"></img>
</div>

*[Quellcode](https://github.com/pfeilbr/ios-enterprise-app-store)*
