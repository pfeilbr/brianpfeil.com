+++
title = "Thinking Architecturally"
slug = "thinking-architecturally"
author = "Brian Pfeil"
date = "2021-05-13"
lastmod = "2021-05-13"
draft = false
categories = []
tags = ["architecture"]
summary = "Thinking Architecturally"

+++


## [Thinking Architecturally](https://www.youtube.com/watch?v=d5bNZX8tpiI)
### Source Resources

* [Thinking Architecturally - Nathaniel Schutta](https://www.youtube.com/watch?v=d5bNZX8tpiI) - youtube
* [Thinking Architecturally: Lead Technical Change Within Your Engineering Team](https://learning.oreilly.com/library/view/thinking-architecturally/9781492034421/) - oreilly book
* [Infrastructure & Ops Superstream Series: CI/CD](https://learning.oreilly.com/videos/infrastructure-ops/0636920531654/) - oreilly video
* [Building Evolutionary Architectures](https://learning.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/) - oreilly book
### Notes ([Thinking Architecturally - Nathaniel Schutta](https://www.youtube.com/watch?v=d5bNZX8tpiI) youtube video)

* AaaS - Architecture-as-a-Service
* many competing agendas
* technology change is a constant
* nobody wants to be on legacy platform
  * java foundational tech for aws, google, twitter, netflix, etc.
* how to evaluate technology
* chasing the new things
* computer science - lifetime learning
* education doesn't end.  lifetime of learning.
* developers have strong opinions
* new and old tech https://youtu.be/d5bNZX8tpiI?t=681
* new - unfinished, unbuggy, unproven
* old - refined, stable, tested
* predictable hype cycle
* how do we know where not to use tech.  takes trial and error.
* asked to build something never built before, using tools we got a few weeks ago, shocked we don't know how long it takes
* developer get bored quickly
* learning keeps it fresh
* commit at some point.  can't constantly experiment
* bleeding edge ... means you will bleed
* pioneers ... ones with arrows in back
* hope is not a strategy
* need to be deliberate when it comes to technology choices
* challenge is how to keep up (*"technology merry go round"*)
* make it part of routine to learn
  * "morning coffee" - peruse the tech news
* attention is most precious resource you have
  * attention is a resource.  it doesn't scale.
  * don't waste your attention.  have to be selective.
* if its a big enough deal, you will hear about it.
* how do we know where to invest our time?
  * be aware of bias
  * skating to where the puck was
* thoughtworks technology radar
  * 20% projects are good space, but fallen out of favor in some circles
* innovation fridays
* architectural briefing - one person does research, presents back to team. short ~45min
  * briefing pans out -> workshop/invest more in it
* greenfield always works.  need to use in target env to understand constraints
* start with low risk capability / not company core
* security - want to stay safe, need to go fast.  time feeds black hats
* policy needed.  measure and enforce, hard part
* pros and cons - always trade-offs
* "it depends" means -> tell me more.  not a stopper.
* ack the negatives.  the most insight is learned from this question
* "You haven't mastered a tool until you understand when it should not be used" - *Kelsey*
* what is the appropriate scale for evaluation. e.g. 1-5
  * harvey balls.  images to remove the *"hard number"* focus effect
    <img src="https://www.evernote.com/l/AAHMoUYQ7Y1Jyq7b1-9Czp1FbEVI4zr0-NQB/image.png" alt="" width="50%" />
  * nobody tells you which criteria to use, up to you, need to make with incomplete information
* architects spread thin, need to scale with principles, north stars, etc.
* arch agile backlash.
* chose tech that can evolve - evolutionary arch
  * create arch with expectation of change. à la werner *"everything fails, all the time"*
  * *"evolutionary arch supports guided, incremental change across multiple dimensions"*
* `[arch]`fitness functions
  * `0: make arch change, 1: eval result, 2: closer to goal? yes -> keep, no -> trash, 3: -> goto 0` *(basic regression iterations as in stats/ML)*
  * set of tests we exec to validate arch. *(arch unit tests)*
  * reminds everyone on the team what's important for your arch
  * informs discussions around tradeoffs
  * need to be visible to team
  * need to be reviewed on regular basis
* just because you can measure it doesn't mean it matters
* avoid resume driven design