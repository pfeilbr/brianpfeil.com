# [brianpfeil.com](https://brianpfeil.com)

## Description

* personal website @ [brianpfeil.com](https://brianpfeil.com)
* this [`personal-website`](.) repo contains the hugo content and configuration
* [`public`](public) directory is a submodule @ <https://github.com/pfeilbr/pfeilbr.github.com> where all static web content is published and hosted using [github pages](https://pages.github.com/).
* [`themes/beautifulhugo`](themes/beautifulhugo) directory is the base hugo theme. It's a submodule @ https://github.com/halogenica/beautifulhugo.  The submodule allows for pulling in updates from this base theme.

## Key Files and Directories

* [`config.yaml`](config.yaml) - site configuration file
* [`public`](public) (*DO NOT DELETE*) - a submodule @ <https://github.com/pfeilbr/pfeilbr.github.com>.  all static web content is published here with github pages used for hosting.
* [`content`](content) - all site content (e.g. yaml files for posts, projects, pages, etc.)
* [`static`](static) - all static content.  all files and directories within are copied to [`public`](public) directory where the site is published
* [`static/CNAME`](static/CNAME) - specifies the custom domain (brianpfeil.com) for github pages to use
* [`themes/beautifulhugo`](themes/beautifulhugo) - base hugo theme. a submodule @ https://github.com/halogenica/beautifulhugo.
* [`themes/hyde`](themes/hyde) (*no longer in use*) - hugo theme.

## Local Development

```sh
# live reload on change.  NOTE: post with draft=true will be displayed
hugo server -D

# visit local site
open http://localhost:1313/
```

## Build and Publish

`./build-and-publish.sh`

> runs hugo to generate site into [`public`](public), commits and pushes all changes to the [`public`](public) submodule.

> NOTE: this script does not commit changes to this [`personal-website`](.) repo

## Commit and Push Source Content Changes

commit hugo content and configuration changes for *this* [`personal-website`](.) repo.

```sh
git add .
git commit -a -m "updates"
git push origin master
```