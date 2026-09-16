+++
author = "Brian Pfeil"
categories = ["Ruby", "playground"]
date = 2014-05-09
description = ""
summary = " "
draft = false
slug = "sinatra-cors-example"
tags = ["ruby","sinatra","cors","api"]
title = "Sinatra CORS Example"
repoFullName = "pfeilbr/sinatra-cors-example"
repoHTMLURL = "https://github.com/pfeilbr/sinatra-cors-example"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/sinatra-cors-example" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/sinatra-cors-example</a>
</div>

## [Sinatra](http://www.sinatrarb.com/) [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS) Example

An example [Sinatra](http://www.sinatrarb.com/) json rest api app showing [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS) support by setting the appropriate HTTP headers

## Core Code

Set appropriate headers in before [filter block](http://www.sinatrarb.com/intro.html#Filters)

```ruby
before do
   content_type :json    
   headers 'Access-Control-Allow-Origin' => '*', 
            'Access-Control-Allow-Methods' => ['OPTIONS', 'GET', 'POST', 'PUT'],
            'Access-Control-Allow-Headers' => 'Content-Type'   
end
```

## Running

	bundle install
	foreman start

## Testing

Run the following from a another non-localhost domain

```javascript
$.get('http://localhost:<port>/movie', function(data) {
	console.log(data);
});
```

```javascript
$.post('http://localhost:<port>/movie', {movie: 'The Godfather'}, function(data) {
	console.log(data);
});
```
