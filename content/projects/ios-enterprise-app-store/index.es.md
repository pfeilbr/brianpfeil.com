+++
title = "iOS Enterprise App Store"
description = "Solución de distribución interna de aplicaciones para miembros del iOS Developer Enterprise Program."
date = 2014-08-04T18:55:46Z
draft = false
weight = 7
+++

Las empresas que son miembros del [iOS Developer Enterpise Program](http://developer.apple.com/programs/ios/enterprise/) pueden distribuir sus aplicaciones internas con su propia App Store mediante la [distribución por aire](http://developer.apple.com/library/ios/#featuredarticles/FA_Wireless_Enterprise_App_Distribution/Introduction/Introduction.html) de Apple. Con esta solución basta con dejar el archivo .ipa de la aplicación y un archivo con su información en un directorio, y queda disponible al instante para que los usuarios la instalen.

El backend es una aplicación web en [Sinatra](http://www.sinatrarb.com/). En el frontend hay una interfaz web integrada hecha con [jQuery Mobile](http://jquerymobile.com/), además de una aplicación nativa de iPhone independiente.

**Aplicación web de la App Store**

<div>
<img style="display: inline; width: 200px;" width="200px" src="images/eas1.png"></img>
<img style="display: inline; width: 200px;" width="200px" src="images/eas3.png"></img>
</div>

**Cliente nativo de iPhone para la App Store**

<div>
<img style="display: inline; width: 200px;" src="images/eas4.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas5.png" width="200px"></img>
<img style="display: inline; width: 200px;" src="images/eas6.png" width="200px"></img>
</div>

*[código fuente](https://github.com/pfeilbr/ios-enterprise-app-store)*
