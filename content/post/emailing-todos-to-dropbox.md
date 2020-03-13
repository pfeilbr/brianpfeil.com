+++
author = "Brian Pfeil"
categories = ["productivity", "dropbox", "appengine"]
date = 2011-11-20T11:48:00Z
description = ""
draft = false
slug = "emailing-todos-to-dropbox"
tags = ["productivity", "dropbox", "appengine"]
title = "Emailing Todos to Dropbox"

+++



Between work and home,I've always got more things to do than I can keep
straight my head. Like most people, I keep a to-do list so I don't have to
worry about forgetting it. My to-do list is a simple bulleted text
([Markdown]) file that I keep in [Dropbox] so I can access it from anywhere.

<pre>
# TODOS

* get gas
* get leaf bags
* send thank you cards

# Completed

* get propane
* get burgers and hot dogs
</pre>

This setup works fairly well, but they're times when I think of something I need to do, but I don't get it into this list because of the time it takes to add it. The usual scenario is that I'm not sitting in front of a computer, and I need to add it using my iPhone. There are plenty of to-do and dropbox text
file editor apps our there to choose from (way too many), but none of them make it fast enough to enter, and fit *my to-do-list-text-file-in-dropbox*
setup.

The best case scenario would be an app, that opens awaiting my next to-do, and I'd just type it in, and it'd add it to my to-do list text file in dropbox in
the right format. I thought about making an app that did just that, but I knew there had to be an easier way. That's when email popped into my head. It's
dead simple, and available everywhere. I'd never have an excuse not to get something on the list. It's also fast and easy to send email.

## Solution

My solution is to send an email to a special "todo" email address where the subject would be the todo item, the email would be processed, and the item added to my to-do list text file in dropbox.

<img width="250px" src="https://img.skitch.com/20111120-xtcdk3fesj6cipmcrbn3u4nr7t.png"></img>
<img width="250px" src="https://img.skitch.com/20111120-qu73ib3nb8endrfssewsp7tmjf.png"></img>

[Google App Engine] lets you run web apps on Google infrastructure for free, and they offer a way to receive and process email. Dropbox provides a [Dropbox Python SDK] to get at your files, which is works out nicely since Python is the primary language used for App Engine development.

You can take a look at the [Google App Engine Receiving Email Documentation], but the gist of it is that an email sent to `NAME@APP.appspotmail.com` will
result in a `HTTP POST` request sent to `/_ah/mail/NAME@APP.appspotmail.com` with the POST body containing the contents of the email. Google provides a nice `InboundMailHandler` class to make handling inbound email a breeze.

The first thing we need to do is to map a handler for inbound emails. I'm using the [Django] Python web framework in my app engine app, which provides
some connivence mechanisms. To map a URL to a handler we add the following to the `urls.py` file.

```language-python
urlpatterns = patterns('',
    (r'^_ah/mail/todo@myapp.appspotmail.com`, 'emailengine.views.todo_email_handler'),
```

We mapped the url to `todo_email_handler` method


```language-python
def todo_email_handler(request):
    if request.POST:
        message = mail.InboundEmailMessage(request.raw_post_data)
        logging.info("Received a message from: " + message.sender)
        if is_whitelisted_email_address(message.sender):
            mgr = DropboxManager()
            mgr.add_todo(message.subject)
            logging.info("Received a message from: " + message.sender + ", Todo:" + message.subject)
    return HttpResponse('ok')
```

In order to prevent anyone from adding to-do items to my list, I added the
`is_whitelisted_email_address` method to restrict processing of emails to only
those that come from me.

```language-python
def is_whitelisted_email_address(email):
    result = False
    for whitelist_email in EMAIL_ADDRESS_WHITELIST:
        if email.lower().find(whitelist_email) != -1:
            result = True

    return result
```

The work to add the to-do item to the TODO.txt file in dropbox is

```language-python
mgr = DropboxManager()
mgr.add_todo(message.subject)
```

I created the `DropboxManager` class as a simple wrapper around the Dropbox
API. This keeps the code tidy, and all the dropbox specific code like the app
key, secret, and token in one place.

## Conclusion

I'm sure one of the many existing to-do list apps fits the needs of most people.  This solution required a little work upfront, but has already proven to be a timesaver.

[Dropbox]: http://dropbox.com
[Dropbox Python SDK]: https://www.dropbox.com/developers/start/setup#python
[Google App Engine]: http://code.google.com/appengine
[Google App Engine Receiving Email Documentation]: http://code.google.com/appengine/docs/python/mail/receivingmail.html
[Markdown]: http://daringfireball.net/projects/markdown/
[Django]: https://www.djangoproject.com/