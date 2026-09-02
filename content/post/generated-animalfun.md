+++
author = "Brian Pfeil"
categories = ["Objective-C", "playground"]
date = 2025-12-31
description = "A simple animal learning program for children on the iPhone"
summary = " "
draft = false
slug = "animal-fun"
tags = ["ios","objective-c","app"]
title = "Animal Fun"
repoFullName = "pfeilbr/animalfun"
repoHTMLURL = "https://github.com/pfeilbr/animalfun"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/animalfun" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/animalfun</a>
</div>


Animal Fun is a simple animal learning program for children. Children learn
about animals by seeing and hearing the sounds an animal makes. It combines an
easy-to-use interface and fun sound effects to entertain children while they
learn.

## iPad Screenshots

![Dog, portrait](https://raw.githubusercontent.com/pfeilbr/animalfun/master/iPad%20Screenshots/dog-portrait-scaled-down-480x640.png)

![Dog, landscape](https://raw.githubusercontent.com/pfeilbr/animalfun/master/iPad%20Screenshots/dog-landscape-scaled-down-480x360.png)

![Horse, portrait](https://raw.githubusercontent.com/pfeilbr/animalfun/master/iPad%20Screenshots/horse-portrait-scaled-down-480x640.png)

![Horse, landscape](https://raw.githubusercontent.com/pfeilbr/animalfun/master/iPad%20Screenshots/horse-landscape-scaled-down-480x360.png)

## Features

* 50+ animals
* touch/tap to change animal
* hear the animal name, the animal sound effect, or the animal name spelled
* individual letters are highlighted as the animal name is being spelled
* set the default sound when the animal is first shown to "Animal Name",
  "Animal Sound", or "Spell Name"

## Usage Considerations

Please make sure the PHONE IS NOT IN SILENT MODE (the switch on the side of the
phone should be up) and Settings | General | Sound Effects is set to BOTH.

You need to use headphones or an external speaker on a first generation iPod
Touch (as it has no external speaker).

## Additional Info

The animal pictures and sound effects are from the free
[Tux Paint](http://tuxpaint.org) desktop (Mac, Windows, Linux) drawing program
for children. You can download it for free at
[http://tuxpaint.org](http://tuxpaint.org).

Animal Fun is free, Open Source software, distributed under the terms of the
GNU [General Public License](https://github.com/pfeilbr/animalfun/blob/master/LICENSE).

## Technical Notes

The [scripts/data_prep.rb](https://github.com/pfeilbr/animalfun/blob/master/scripts/data_prep.rb) file is used for preparing the
image and audio files from the TuxPaint stamps package and also generating json
metadata used by the Animal Fun application.
[SoX](http://sox.sourceforge.net/) is used to convert the .ogg audio files to
.aiff.

