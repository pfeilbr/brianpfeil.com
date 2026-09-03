+++
title = "iOS Enterprise App Store"
description = "Soluzione di distribuzione interna delle app per chi aderisce all'iOS Developer Enterprise Program."
date = 2014-08-04T18:55:46Z
draft = false
weight = 7
+++

Le aziende iscritte all'[iOS Developer Enterpise Program](http://developer.apple.com/programs/ios/enterprise/) possono distribuire le app ai propri dipendenti tramite un App Store interno, usando la [distribuzione over-the-air](http://developer.apple.com/library/ios/#featuredarticles/FA_Wireless_Enterprise_App_Distribution/Introduction/Introduction.html) di Apple. Con questa soluzione basta mettere il file .ipa dell'app e un file con le sue informazioni in una cartella, e l'app è subito installabile dagli utenti.

Il backend è un'applicazione web [Sinatra](http://www.sinatrarb.com/). Sul frontend c'è un'interfaccia web integrata in [jQuery Mobile](http://jquerymobile.com/) e, in aggiunta, un'app nativa per iPhone.

**App Store come applicazione web**

<div>
<img style="display: inline; width: 200px;" width="200px" src="images/eas1.png"></img>
<img style="display: inline; width: 200px;" width="200px" src="images/eas3.png"></img>
</div>

**Client nativo per iPhone**

<div>
<img style="display: inline; width: 200px;" src="images/eas4.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas5.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas6.png" width="200px"></img>
</div>

*[codice sorgente](https://github.com/pfeilbr/ios-enterprise-app-store)*
