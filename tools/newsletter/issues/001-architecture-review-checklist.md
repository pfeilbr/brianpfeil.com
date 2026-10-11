---
subject: "The 41 questions I ask in every architecture review"
url: https://brianpfeil.com/architecture/architecture-review-checklist/
---
I've sat on the reviewing side of a few hundred cloud architecture reviews. Different teams, vendors and business problems, but the same forty-odd questions come up every time. I wrote them down as a checklist.

**Use it two ways.** If you're presenting, answer every question before the meeting, and the review becomes a conversation instead of an interrogation. If you're reviewing, it's a starting point: add the questions your organisation keeps having to ask.

The questions fall into eight groups:

1. **Compute:** why not something more managed? Could this be SaaS? Why not serverless?
2. **Vendor and ownership:** who patches it, who supports it, and where the responsibility splits.
3. **Identity, access and secrets:** is any automation running on a person's credentials?
4. **Data and compliance:** classification, encryption, retention, and keeping sensitive data out of the logs.
5. **Networking:** anything inbound other than 443 needs a reason.
6. **Resilience:** RTO and RPO, multi-AZ, idempotent handlers, dead-letter queues.
7. **Observability:** every error metric should page someone or trigger self-healing.
8. **Delivery and cost:** including the two numbers most estimates leave out, idle cost and data transfer.

What gets a team sent back is rarely a bad idea. It's a **missing answer**, usually about failover, backups, alarms, the support model or cost.

And one rule I hold to: a concession is fine, but write it down with a date to fix it. An undated exception is a permanent one.

**[Read the full checklist →](https://brianpfeil.com/architecture/architecture-review-checklist/)**

Thanks for reading,
Brian
