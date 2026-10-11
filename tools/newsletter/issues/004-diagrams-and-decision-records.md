---
subject: "Diagrams and decision records reviewers trust"
url: https://brianpfeil.com/architecture/diagrams-and-decision-records/
---
Two artefacts do most of the work in an architecture review: the **diagram**, which shows what you're building, and the **decision record**, which shows why. Get both right and the meeting is about trade-offs, not archaeology.

**For diagrams:**

- **Use the reference-architecture style** with your cloud provider's official icons. Reviewers read that visual language fluently.
- **Number the flow.** Put a number on every arrow of the main path. Then a reviewer can say "at step 4, what happens if…" and everyone is looking at the same place.
- **Draw the boundaries:** internet, company, on-premises, accounts, regions, subnets. Most security questions are really questions about boundaries.
- **Draw a small set, not one poster:** the core flow, build and deploy, availability and recovery, and vendor lifecycle if relevant.

If a cross-cutting concern such as secrets, alarms, backups or cost isn't on any diagram or page, reviewers will assume it hasn't been designed. Usually they're right.

**For decisions,** write a short architecture decision record (ADR) whenever you choose between real options: a database, a compute rung, a vendor, or a concession you plan to fix later. Four habits make them useful:

1. Include the options you rejected. They stop the same debate from happening again.
2. Name the drivers before the decision.
3. Supersede, don't edit. The history is the value.
4. Record concessions with a date. "We'll run it on servers for now" is a decision; "…and move by Q3" makes it a plan.

The guide includes a copy-paste ADR template.

**[Read the guide →](https://brianpfeil.com/architecture/diagrams-and-decision-records/)**

Related: [How to prepare for an architecture review](https://brianpfeil.com/architecture/prepare-for-an-architecture-review/)

Thanks for reading,
Brian
