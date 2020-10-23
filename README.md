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
# start local hugo dev server.  live reload on change.
site run-local # will automatically open local server @ http://localhost:1313/

# create new post. *remember to change front matter `draft=false` to publish*
site post -t 'hello post'
```

## Build and Publish

`site publish [-m commit_message]`

* runs hugo to generate site into [`public`](public)
* commits and pushes all changes to the [`public`](public) submodule.
* commits and pushes all changes to *this* [`personal-website`](.) top-level repo.

## [`site`](site) script

* a script for authoring and publishing site content
* after script updates run `make install-site-script` to install to `~/bin`
* `site generate-posts-from-repos`
    > `~/create-blog-post-from-repo/.env` - edit post titles, tags, casing, etc.