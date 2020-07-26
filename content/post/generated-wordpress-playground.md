+++
author = "Brian Pfeil"
categories = ["PHP", "playground"]
date = 2019-10-22
description = ""
summary = "learn Wordpress"
draft = false
slug = "wordpress"
tags = ["wordpress","github",]
title = "Wordpress"
repoFullName = "pfeilbr/wordpress-playground"
repoHTMLURL = "https://github.com/pfeilbr/wordpress-playground"
truncated = true

+++


learn and experiment with all things [WordPress](https://wordpress.com/) and [WordPress VIP](https://wpvip.com/) (aka Enterprise WordPress)

## Running using Docker Compose

```sh
# ensure docker is up and running

# start
docker-compose up -d

# admin ui (login: admin/password01)
open http://localhost:8000/wp-admin

# site
open http://localhost:8000

# root rest api routes
curl http://localhost:8000/index.php?rest_route=/ | jq '.'

# rest api routes
curl http://localhost:8000/\?rest_route\=/wp/v2 | jq '.'

# rest api posts example
curl http://localhost:8000/?rest_route=/wp/v2/posts | jq '.'

# stop
docker-compose down
```

---

## Extending WP REST API | Adding Custom Endpoints | Custom Plugin Example

based on [Adding Custom Endpoints](https://developer.wordpress.org/rest-api/extending-the-rest-api/adding-custom-endpoints/)

1. create [`wp-root/wp-content/plugins/myplugin.php`](wp-root/wp-content/plugins/myplugin.php)

    > if needed, copy to "live" plugins directory
    ```sh
    cp wp-root/wp-content/plugins/myplugin.php html/wp-content/plugins/myplugin.php
    ```
1. activate via Admin | Plugins
    ![](assets/images/admin-plugin-01.png)
1. access custom endpoint <http://localhost:8000/index.php?rest_route=/myplugin/v1/author/1>
    ![](assets/images/custom-endpoint-response-json.png)

---

## Running using [VVV (Varying Vagrant Vagrants)](https://varyingvagrantvagrants.org/)

### Setup

1. install [System Requirements](https://varyingvagrantvagrants.org/docs/en-US/installation/software-requirements/)
1. execute [Installation](https://varyingvagrantvagrants.org/docs/en-US/installation/) steps


### Running

root directory path `~/vagrant-local`

1. `vagrant up`
1. add VirtualBox port mappings `0.0.0.0:80 -> 80`
    ![](assets/images/Port_Forwarding_Rules_and_vagrant-local_39d50a0a4d6_-_Network_and_Oracle_VM_VirtualBox_Manager.png)
1. update `/etc/hosts` to point to `127.0.0.1`

    `sudo sed -i.bu 's/192.168.50.4/127.0.0.1/g' /etc/hosts`
    ![](assets/images/hosts_—_notes.png)    
1. visit <http://vvv.test>

> Shouldn't need to do the `/etc/hosts` and VirtualBox port mapping steps.  This is a workaround to deal with an iss where macOS ignores the entries added by the `vagrant-hostsupdater` plugin in `/etc/hosts` file.


### stopping

* `vagrant halt`
    > this removes `/etc/hosts` entries


---

### Changes

#### Allow logging in to a WP VIP site (e.g. <http://WP-VIP-SITE/wp-admin>) with admin / password.

changed `wpcom_vip_is_restricted_username` @ `WP-VIP-SITE/public_html/wp-content/mu-plugins/security.php` to

```php
function wpcom_vip_is_restricted_username( $username ) {
	// return 'admin' === $username
	// 	|| WPCOM_VIP_MACHINE_USER_LOGIN === $username
	// 	|| WPCOM_VIP_MACHINE_USER_EMAIL === $username;
	return false;
}
```

#### Remove `VIP_MAINTENANCE_MODE` not defined error message showing in wp-admin and site UIs

added the following to `WP-VIP-SITE/public_html/wp-content/client-mu-plugins/plugin-loader.php` to get rid of 
`VIP_MAINTENANCE_MODE` not defined error message showing in wp-admin and site UIs.

```php
define( 'VIP_MAINTENANCE_MODE', false );
```

---

## Resources

* [Quickstart: Compose and WordPress](https://docs.docker.com/compose/wordpress/)
* [WordPress VIP Documentation](https://wpvip.com/documentation/)
* [WordPress | REST API Handbook](https://developer.wordpress.org/rest-api/)
* [Block Editor Handbook](https://developer.wordpress.org/block-editor/)
* [WordPress/gutenberg](https://github.com/WordPress/gutenberg)
    * [packages/block-library](https://github.com/WordPress/gutenberg/blob/master/packages/block-library/README.md) - Block library for the WordPress editor.
* [WordPress Storybook site](https://wordpress.github.io/gutenberg/?path=/story/docs-introduction--page)
* [developer.wordpress.org](https://developer.wordpress.org/)
* [codex.wordpress.org](https://codex.wordpress.org/)
* [Adding Custom Endpoints](https://developer.wordpress.org/rest-api/extending-the-rest-api/adding-custom-endpoints/)
* [WPGraphQL](https://docs.wpgraphql.com/) - graphql API for WP
* [Automattic/vip-go-mu-plugins](https://github.com/Automattic/vip-go-mu-plugins) - The development repo for mu-plugins used on the VIP Go platform.
* [Automattic/vip-go-mu-plugins-built](https://github.com/Automattic/vip-go-mu-plugins-built) - The generated repo for mu-plugins used on the VIP Go platform
* [Theme Handbook / Advanced Theme Topics / Child Themes](https://developer.wordpress.org/themes/advanced-topics/child-themes/)
