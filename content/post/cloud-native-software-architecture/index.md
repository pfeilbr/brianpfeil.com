+++
title = "Cloud Native Software Architecture"
slug = "cloud-native-software-architecture"
author = "Brian Pfeil"
date = "2020-07-28"
lastmod = "2020-07-28"
draft = false
categories = ["architecture", "cloud"]
tags = ["architecture", "cloud"]
summary = "A cheatsheet/reference for cloud native software architecture"

+++

A cheatsheet/reference for cloud native software architecture.

**architecture**

> how the components are assembled and organized. This will be done in a way that meets the quality attributes.

---

<!-- TOC -->

- [Key Questions](#key-questions)
- [Organization Considerations](#organization-considerations)
- [Quality Attributes *(\*ities and friends)*](#quality-attributes-ities-and-friends)
- [Patterns](#patterns)
  - [event-sourcing](#event-sourcing)
    - [Core Design Decisions](#core-design-decisions)
    - [Resources](#resources)
  - [Hexagonal](#hexagonal)
    - [Resources](#resources-1)
- [Topics / Concepts / Terms](#topics--concepts--terms)
  - [Database](#database)
  - [Shuffle Sharding](#shuffle-sharding)
  - [Constant Work](#constant-work)
  - [Canary](#canary)
- [Resources](#resources-2)
  - [Books (*oreilly.com*)](#books-oreillycom)
  - [Websites](#websites)

<!-- /TOC -->

---

## Key Questions

* who are the users?
* what devices and form factors will be used?
* what is the context of their usage?
* scale and growth?
* who are the main actors in the system (domain objects - e.g. orders, products, etc.)?
* data classifications (PII)?
* data types and sizes (relation records, documents, media files, etc.)?
* what is the time frame for delivery?
* is there an existing product / SaaS / open-source / etc. that provides the solution or a portion / components of it
* capacity estimation & constraints?
* functional requirements?
* Non Functional Requirements - Latency, Consistency, Availability, High Throughput, etc.
* what is explicitly **out of scope**
* organization and teams structure

> see [System Design: DoorDash — a prepared food delivery service](https://medium.com/partha-pratim-sanyal/system-design-doordash-a-prepared-food-delivery-service-bf44093388e2) for good reference

---

## Organization Considerations

* engineering (application & platform)
* operations (application & platform)

---

## Quality Attributes *(\*ities and friends)*

* reliability - ability to continue to operate under predefined conditions
* availability - ratio of the available system time to the total working time
* scalability - ability of the system to handle load increases without decreasing performance
* efficiency
* performance
* security
* cost
* interoperability
* correctness
* maintainability
* readability
* extensibility
* testability

## Patterns

modern cloud native architecture patterns *as of July 2020*

---

### event-sourcing

> Capture all changes to an application state as a sequence of events.

#### Core Design Decisions

* Domain Entities and Events
    * popular method is via [Event Storming](https://en.wikipedia.org/wiki/Event_storming)
* Event Content
    * each event stores delta state
    * each event stores full state
        * idempotent is easy to solve for duplicate events
* Total Ordering (ordered stream of events - ledger)
    * ensure all event are processed in order.  this is needed for causal relationships.
    * e.g. ordering matters for two messages related to the same entity

#### Resources

* [Scaling Event Sourcing for Netflix Downloads, Episode 1](https://netflixtechblog.com/scaling-event-sourcing-for-netflix-downloads-episode-1-6bc1595c5595)
* [Scaling Event Sourcing for Netflix Downloads, Episode 2](https://netflixtechblog.com/scaling-event-sourcing-for-netflix-downloads-episode-2-ce1b54d46eec)
* [InfoQ | Scaling Event Sourcing for Netflix Downloads | Video + Presentation](https://www.infoq.com/presentations/netflix-scale-event-sourcing) - shows in detail how they implemented event sourcing backed by cassandra
* [matrinfowler.com | Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
* [Pattern: Event sourcing](https://microservices.io/patterns/data/event-sourcing.html)
* [EventBridge Storming — How to build state-of-the-art Event-Driven Serverless Architectures](https://medium.com/serverless-transformation/eventbridge-storming-how-to-build-state-of-the-art-event-driven-serverless-architectures-e07270d4dee) - approach to defining the Events, Boundaries and Entities in your business domain
* [Decomposing the Monolith with Event Storming](https://medium.com/capital-one-tech/event-storming-decomposing-the-monolith-to-kick-start-your-microservice-architecture-acb8695a6e61)

---

### Hexagonal

the ports and adapters architecture.  decouples core domain logic from specific storage, database, protocol, etc.

#### Resources

* [Hexagonal Architecture: three principles and an implementation example](https://blog.octo.com/en/hexagonal-architecture-three-principles-and-an-implementation-example/)

---

## Topics / Concepts / Terms

### Database

* [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)
    * Consistency: Every read receives the most recent write or an error
    * Availability: Every request receives a (non-error) response, without the guarantee that it contains the most recent write
    * Partition tolerance: The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes
* [Serializability](https://en.wikipedia.org/wiki/Serializability)
* [Snapshot isolation](https://en.wikipedia.org/wiki/Snapshot_isolation)
* [Multiversion concurrency control](https://en.wikipedia.org/wiki/Multiversion_concurrency_control)
* [Things I Wished More Developers Knew About Databases](https://medium.com/@rakyll/things-i-wished-more-developers-knew-about-databases-2d0178464f78)

---

### Shuffle Sharding

limits / isolates tenants in a multi-tenant system so they don't negatively impact other tenants.  method of assigning tenant to resources.

**Resources**

* [Workload isolation using shuffle-sharding](https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/?did=ba_card&trk=ba_card)

### Constant Work

* overprovision resources to the point where it would operate correctly even if an availability zone were to be unavailable
* if AZ becomes unavailable, no new resources need to be provisioned, just a quick re-routing.  you are essentially always operating the infrastructure for failure mode (active-active)

**Resources**

* [Static stability using Availability Zones](https://aws.amazon.com/builders-library/static-stability-using-availability-zones)

---

### Canary

> A canary release is a technique to reduce the risk from deploying a new version of software into production. A new version of software, referred to as the canary, is deployed to a small subset of users alongside the stable running version. Traffic is split between these two versions such that a portion of incoming requests are diverted to the canary. This approach can quickly uncover any problems with the new version without impacting the majority of users.

**Resources**

* [Automated Canary Analysis at Netflix with Kayenta](https://netflixtechblog.com/automated-canary-analysis-at-netflix-with-kayenta-3260bc7acc69)

---

## Resources

### Books (*oreilly.com*)

* [Fundamentals of Software Architecture](https://learning.oreilly.com/library/view/fundamentals-of-software/9781492043447/)
* [Clean Architecture: A Craftsman's Guide to Software Structure and Design, First Edition](https://learning.oreilly.com/library/view/clean-architecture-a/9780134494272/)
* [Software Architecture Patterns](https://learning.oreilly.com/library/view/software-architecture-patterns/9781491971437)
* [Building Evolutionary Architectures](https://learning.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/)
* [Clean Architecture: A Craftsman's Guide to Software Structure and Design, First Edition](https://learning.oreilly.com/library/view/clean-architecture-a/9780134494272/)
* [Domain-Driven Design: Tackling Complexity in the Heart of Software](https://learning.oreilly.com/library/view/domain-driven-design-tackling/0321125215/)
* [Microservices Patterns](https://learning.oreilly.com/library/view/microservices-patterns/9781617294549/)
* [Patterns of Enterprise Application Architecture](https://learning.oreilly.com/library/view/patterns-of-enterprise/0321127420/)
* [Refactoring: Improving the Design of Existing Code](https://learning.oreilly.com/library/view/refactoring-improving-the/9780134757681/)
* [Design Patterns: Elements of Reusable Object-Oriented Software](https://learning.oreilly.com/library/view/design-patterns-elements/0201633612/)
* [Designing Distributed Systems](https://learning.oreilly.com/library/view/designing-distributed-systems/9781491983638)

* [Designing Distributed Control Systems: A Pattern Language Approach (Wiley Software Patterns Series)](https://www.amazon.com/Designing-Distributed-Control-Systems-Language/dp/1118694155/)

### Websites

* [martinfowler.com](https://martinfowler.com/)
* [AWS Architecture Center](https://aws.amazon.com/architecture)
* [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture)
* [Amazon Builders' Library](https://aws.amazon.com/builders-library/?cards-body.sort-by=item.additionalFields.customSort&cards-body.sort-order=asc)
* [Azure Architecture Center](https://docs.microsoft.com/en-us/azure/architecture/)
* [medium | articles tagged with "software architecture"](https://medium.com/tag/software-architecture)
* [C4 model for visualizing software architecture](https://c4model.com/)
