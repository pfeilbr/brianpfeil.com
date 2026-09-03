+++
title = "iOS Enterprise App Store"
description = "Une solution de distribution d'applications internes pour les membres de l'iOS Developer Enterprise Program."
date = 2014-08-04T18:55:46Z
draft = false
weight = 7
+++

Les entreprises membres de l'[iOS Developer Enterpise Program](http://developer.apple.com/programs/ios/enterprise/) peuvent distribuer leurs applications internes via leur propre App Store, grâce à la [distribution par voie hertzienne](http://developer.apple.com/library/ios/#featuredarticles/FA_Wireless_Enterprise_App_Distribution/Introduction/Introduction.html) d'Apple. Avec cette solution, il suffit de déposer le fichier .ipa de l'application et un fichier décrivant celle-ci dans un répertoire : elle est aussitôt installable par les utilisateurs.

Le backend est une application web [Sinatra](http://www.sinatrarb.com/). Côté frontend, on trouve une interface web [jQuery Mobile](http://jquerymobile.com/) intégrée, ainsi qu'une application iPhone native distincte.

**Application web App Store**

<div>
<img style="display: inline; width: 200px;" width="200px" src="images/eas1.png"></img>
<img style="display: inline; width: 200px;" width="200px" src="images/eas3.png"></img>
</div>

**Client App Store natif pour iPhone**

<div>
<img style="display: inline; width: 200px;" src="images/eas4.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas5.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas6.png" width="200px"></img>
</div>

*[code source](https://github.com/pfeilbr/ios-enterprise-app-store)*
