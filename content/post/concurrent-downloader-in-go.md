+++
author = "Brian Pfeil"
categories = ["golang", "concurrency"]
date = 2015-03-26T01:36:21Z
description = ""
draft = false
slug = "concurrent-downloader-in-go"
tags = ["golang", "concurrency"]
title = "Concurrent Downloader in Go"

+++


[Go](https://golang.org/) has been getting a lot of traction among the [coding elite](https://medium.com/code-adventures/farewell-node-js-4ba9e7f3e52b) due to it's simplicity, speed, and most touted, it's ability to enable concurrent solutions.

Go is a very small language.  If you have experience with a few languages, you can learn in a few days and fit and keep it all in your head.  With most other languages, I'm accustomed to looking up documentation or examples on stackoverflow while I code.  With Go, I find I don't do it as much.

It's a language influenced by C and the rest of curly brace family of languages.  It compiles down into standalone binaries with no dependencies.  I can't emphasize how great this is for building cross-platform tools.  You write your code once, and can cross-compile to any of core three OSs ([osx](https://www.google.com/search?q=osx), [linux](https://www.google.com/search?q=linux), [windows](https://www.google.com/search?q=windows)) from any one of them.  No need to run a windows VM to build for windows.

The most visible feature and probably most discussed is it's concurrency model.  It provides the primitive [channel](https://gobyexample.com/channels) construct, with along with the [syntax](https://gobyexample.com/channels) makes tackling concurrency problems more intuitive than the typical thread construct provided by a majority of languages.

In order to get a thorough understanding of concurrency in go, I thought of a real world problem that lends itself to being solved via concurrency.  The [ATP](http://atp.fm/episodes/98) podcast with [Marco Arment](http://marco.org) was food for thought for an example real world.  Downloading web content and indexing it in an efficient manner is a problem many web based services do.  The process of indexing web content is computationally expensive, and only doing it when neccessary is desired.  If the web content hasn't changed, then we shouldn't waste compute resources indexing the content.  One way to detect this is by doing an MD5 hash of the web contents (HTML page) and only index it if it's changed.

The first step is fetching the contents of the web resource via a URL.  The built-in `net/http` package turns this into a one-liner

	resp, err := http.Get(url)

We can then get the body

	body, err := ioutil.ReadAll(resp.Body)
   
and create an MD5 hash of it

	hash := md5.Sum(body)
    

Now onto the interesting part of parallelizing.  We create a simple structure to hold the information needed to do the work.  In this case it's simply a URL

	type URLJob struct {
		url string
	}


We also need to create a structure to hold the results

	type URLResult struct {
		URL  string
		Body string
		MD5  string
	}

With these in place we con now focus on the work with our `worker` function.

	func worker(id int, jobs <-chan URLJob, results chan<- URLResult) {
		for j := range jobs {
			fmt.Println("worker", id, "processing job", j.url)
			results <- fetch(j.url)
		}
	}

Let's focus on the arguments.  `jobs <-chan URLJob` is an array of channels where you can send `URLJob` instances to it.  `results chan<- URLResult` is an array of channels where we can send the results to.

We then invoke via a goroutine

	go worker(w, jobs, results)

This is where the magic happens.  `go func` creates a goroutine that is ran concurrently by the Go runtime.

In our example, waiting on the network to respond with the contents of the URL is the limiting factor.  In this case, all these http GET requests will be fired off essentially at once, and as the responses return our `results` channel array will be updated.  You could request 1000s of URLs at a time and assuming the response contents are not huge, this wouldn't move the needle noticably on CPU and memory for a reasonably sized machine.

Parallelism is baked into all hardware these days and is the way the computing hardware industry holds true to Moores law.  Modern languages like Go need to surface these advances, but without the usual cognitive load of using threads.  The holy grail of writing your code as if everything is syncronous and having it parallelized automatically for you to make use of all the cores, etc. seems a ways off or most likely will never happen.  In the meantime Go is making a good run at it and moving us forward in this space.

Example code for the concurrent downloader example is on github at [pfeilbr/concurrent-downloader](https://github.com/pfeilbr/concurrent-downloader).