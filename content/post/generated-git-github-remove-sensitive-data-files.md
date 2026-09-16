+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2020-11-04
description = ""
summary = " "
draft = false
slug = "remove-sensitive-files-from-git-history"
tags = ["git","github","security"]
title = "Remove Sensitive Files from Git History"
repoFullName = "pfeilbr/git-github-remove-sensitive-data-files"
repoHTMLURL = "https://github.com/pfeilbr/git-github-remove-sensitive-data-files"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/git-github-remove-sensitive-data-files" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/git-github-remove-sensitive-data-files</a>
</div>


how to delete sensitive files or replace credentials in sensitive files
with "***REMOVED***"

## Prerequisites

* BFG Repo-Cleaner - `brew install bfg`

---

**Understand the following before starting**

> By default the BFG doesn't modify the contents of your latest commit on your master
  (or 'HEAD') branch, even though it will clean all the commits before it.

> That's because your latest commit is likely to be the one that you deploy to production, and a simple deletion of a private credential or a big file is quite likely to result in broken code that no longer has the hard-coded data it expects - you need to fix that, the BFG can't do it for you. Once you've committed your changes- and your latest commit is clean with none of the undesired data in it - you can run the BFG to perform it's simple deletion operations over all your historical commits.

---

## Procedure

1. delete/remove/replace the sensitive data/credentials/etc. and commit
2. Run the following to update / remove from  commit history
    ```sh
    REPO_NAME="git-scratchpad"
    cd ~/projects
    git clone --mirror https://github.com/pfeilbr/$REPO_NAME.git
    bfg --replace-text ./bfg-replace-text.txt $REPO_NAME.git
    cd $REPO_NAME.git
    git reflog expire --expire=now --all && git gc --prune=now --aggressive
    git push
    cd ..
    rm -fr $REPO_NAME.git
    cd $REPO_NAME
    git pull
    code .

    # actual example commands
    rm -fr activity-hub
    git clone --mirror https://github.com/pfeilbr/git-scratchpad.git
    bfg --replace-text ./bfg-replace-text.txt git-scratchpad.git
    cd git-scratchpad.git
    git reflog expire --expire=now --all && git gc --prune=now --aggressive
    git push
    cd ..
    rm -fr git-scratchpad.git
    gh repo clone pfeilbr/git-scratchpad
    code git-scratchpad
    ```

## Resources

* [Removing sensitive data from a repository - GitHub Docs](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/removing-sensitive-data-from-a-repository)
* [BFG Repo-Cleaner by rtyley](https://rtyley.github.io/bfg-repo-cleaner/)
* [How to remove sensitive files from GitHub commit history?](https://itnext.io/how-to-remove-sensitive-files-from-github-commit-history-638a3f291f74)
