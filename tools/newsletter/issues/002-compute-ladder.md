---
subject: "Serverless-first, then work backwards"
url: https://brianpfeil.com/architecture/compute-ladder/
---
When a team asks "where should this run?", I don't start with their stack. I start at the top of a ladder and ask what stops us from staying there:

1. **SaaS:** someone else runs all of it.
2. **Serverless and managed services:** functions, workflows, queues, managed databases.
3. **Containers:** batch, then serverless containers, then orchestrators.
4. **Servers:** you patch, scale and babysit it.

**The rule: design the ideal, most-managed version first. Then work backwards, one rung at a time, and only for a constraint you can name.**

The mistake I see most often is the reverse: start from what the team already runs, and only move up if someone insists. That produces architectures shaped by habit rather than by the problem.

Every step up hands a whole category of work to someone else. Going from servers to containers, you stop owning OS images and most patching. From containers to serverless, you stop owning cluster capacity, scaling policy and idle cost. From serverless to SaaS, you stop owning the code itself.

Serverless architecture is mostly **composition, not programming**. You wouldn't write your own hash map, so don't write your own queue, retry loop or workflow engine. Prefer configuration over code, because code is a liability: it has to be tested, patched and owned.

Good reasons to step down a rung: execution limits, a vendor product that only ships as an image, real local state, or a proven cost crossover. Reasons I wouldn't accept: familiarity, "we might need it later", or a design that only needs a server because it polls on a timer.

**[Read the guide →](https://brianpfeil.com/architecture/compute-ladder/)**

Thanks for reading,
Brian
