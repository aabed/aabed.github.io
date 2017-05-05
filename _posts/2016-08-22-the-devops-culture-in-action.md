---
layout: post
title: "The DevOps culture in action"
description: ""
category:
tags: ["DevOps","culture"]
---
{% seo %}
{% include JB/setup %}

## DevOps culture, I guess

A lot of people I know always asks me about DevOps, what is it all about

Well, I won't say I am a good story teller but I am never out of stories, So let me tell you a few stories from my current job that hopefully will help you get a better understanding of the DevOps movement, culture, practice methodology or whatever you call it

And that I guess are presenting the culture


### Elasticsearch

We have a component that reads data from Elasticsearch before I come to the company, they used to use elastic.co cloud so the connection string was <subdomain>.found.io


And the driver will automatically append 9200 to the domain name

We wanted to host our own Elasticsearch cluster, without going into details I ended up making it a path on a domain like "example.com/elasticsearch" when we tried to connect to it we ended up with "example.com/elasticsearch:9200" which is not valid

I asked the developers to change the code to use the path instead and git rid of that 9200 the driver appends, but they replied that the driver doesn't support this

So I went and started digging at https://www.elastic.co/guide/en/elasticsearch/client/javascript-api/current/index.html


To find that this applicable, and submitted a patch to the component, which was accepted and made it's way to the production


The tricky part was that I don't know javascript or coffeescript but with a few trials and errors I get it to work


### The empty log

We changed our cloud provider, after the migration while we are doing a sanity test we were unable to get it to work, requests times out and we have empty logs

So I went back to old builds trying to see if there is a specific change that may work on the old provider but not on the new one

once I found a working build I called for a developer to explain to me the code and what possibly be the problem

A few minutes a developer came to my desk, I showed her the commit in question and she pointed out an environmental variable the code reads and said that this is the only change that might break the server, I went to check it's value to find it correct with the developer saying that the value is correct and she can't tell what is happening

The configuration was an IP lookup service I tried to curl it from the new servers

and it was unreachable

I suggested to use maxmind Database inside our code to, I've dealt with it back when I used to work on honeypots and contributing to  [MHN](https://github.com/threatstream/mhn)


I went to another developer to start working on that code, then after explaining to him what to do he came up with a better solution "Why don't we write our own service for IP lookup"


I asked if he would like me to work on it and he said yes this will be great, So I wrote the service and made sure it gives the same output as the external service did, with the help of the developer and a few questions here and there I got it working

### Misconfiguration

We use consul to store our configurations, one of the components we misbehaving

A developer traced the problem back to consul, and fixed it himself getting everything back to work

### Elastic again

But this time it was scala, the code is not working, after digging I found that you have to pass the cluster name to the driver, which the test cluster didn't have and that's why their code was working just fine, so looking into the driver's doc I was able to write a small patch that got it to work



## Conclusion

You see the pattern in those stories, there was no "it works on my machine"

There was no "it's an operations problem" or "it's a code problem"

Everyone use whatever skills they have to get things to work
