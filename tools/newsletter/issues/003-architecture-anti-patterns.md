---
subject: "17 cloud anti-patterns I keep flagging (and what to do instead)"
url: https://brianpfeil.com/architecture/architecture-anti-patterns/
---
None of these is a disaster on its own. Each one adds operational work, hides a failure mode, or makes the next change harder, and they compound. Here are the ones I flag most often in reviews, with the fix I recommend:

- **Glue code in a function.** If a function only moves a message from one managed service to another, let the services talk directly.
- **One big function that does many steps.** Use a workflow engine, one step per function. Retries, timeouts and per-step visibility come for free.
- **A synchronous API in front of a long job.** Accept onto a queue, return an ID, and let the client poll or be notified.
- **Storage events wired straight to a function.** Put a queue in between: stable storage first.
- **Calling someone else's flaky API directly.** Go through a queue, so their outage becomes your backlog, not your outage.
- **Polling and cron.** Use event-driven triggers. Polling is either late or wasteful, and it's often the only reason the design needs a server.
- **Credentials in environment variables or on disk.** Use a secrets manager, read at runtime by a narrowly scoped role, with rotation on.
- **Automation on a person's credentials.** Use roles with temporary credentials. When the person leaves, nothing breaks.
- **SSH through a jump host.** Use a session manager: no inbound ports, no shared keys, every session logged.
- **Raw CSV as the long-term format.** Use Parquet with lifecycle rules.
- **Database links between systems.** Use an API or events.

The common thread: **prefer managed services composed through configuration, connected by queues and events, and accessed through roles.** Most anti-patterns are a missing queue, a missing role, or code standing in for a service that already exists.

**[See all seventeen →](https://brianpfeil.com/architecture/architecture-anti-patterns/)**

Thanks for reading,
Brian
