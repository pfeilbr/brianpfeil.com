# Security

brianpfeil.com is a static site: Hugo builds it, GitHub Pages serves it, and
the /media/ files come from a private S3 bucket behind CloudFront. There are
no accounts, no server-side code and no visitor data beyond Google Analytics.

## Reporting a problem

Please don't open a public issue for anything exploitable (a leaked secret,
a way to change what the site serves, a hole in the automation). Instead,
send a private message through one of the profiles on
<https://brianpfeil.com/about/> with what you found and how to reproduce it.
You'll get an answer within a few days.

Useful to report:

- a credential, token or personal detail visible in the site, a feed, the
  repository or its history;
- a way to make a page load or link to something it shouldn't (a hijackable
  host, an open redirect in the `/apps/<key>/` short links);
- a workflow in `.github/workflows/` that could be made to run untrusted code
  with write access.

Not in scope: missing HTTP headers that GitHub Pages doesn't let a site set,
and findings in third-party sites the pages link to.

## What is already in place

- The build fails if an AWS account id, a personal path or a secret-shaped
  string reaches the built site (`tools/site-check/check_structure.py`).
- Hugo may not fetch remote URLs or run anything but `git` at build time
  (`security` in `config.yaml`).
- Third-party actions are pinned to commit SHAs; Dependabot proposes updates
  after a week's cooldown; CI runs `govulncheck` and `pip-audit`.
- The S3 buckets are private, TLS-only and encrypted (`infra/`).
