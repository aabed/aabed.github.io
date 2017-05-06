---
layout: post
title: "Using envconsul with docker to configure your app using environmental variables"
description: "How to use envconsul to configure your app/containers using env variable hosted on consul as ket/value"
category:
tags: ['docker','envconsul','consul']
---
{% seo %}
{% include JB/setup %}


If you are delivering your apps using the 12factor methodology you should be using environmental variables to configure your apps
Also if you are delivering your apps in form of Docker containers it is always easier to configure the containers using environmental variables even if you are not using the 12factor
for example

MySql
{% highlight bash %}
$ docker run --name some-mysql -v /my/custom:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:tag
{% endhighlight %}


Configuring your app using environmental variables has many benefits, in this post I will discuss the benefit of having them in a centralized place

* You can change the configurations of a fleet of containers all at once
* This can make feature toggling a piece of cake
* Switching to a new service and roll back is much easier now `API_SERVER=new.api.server` or `API_SERVER=old.api.server`

## Envconsul
envconsul provides a convenient way to populate values from Consul into a child process environment using the envconsul daemon.

The daemon envconsul allows applications to be configured with environment variables, without having knowledge about the existence of Consul. This makes it especially easy to configure applications throughout all your environments: development, testing, production, etc.

Basically envconsul will connect to consul,read the variables and then fork(clone) your app and then inject that environment into your app, and keeps listening for changes on consul server, if any change happens it will send signal to your app (default is HUP)

![alt img1](https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/envconsul_1.png) ![alt img2](https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/envconsul_2.png)


let's try it with a sample python code
First let's run a development consul server

{% highlight shell %}
docker run -d  -p 8500:8500 consul
{% endhighlight %}

Here is a small code that will print the variable upon http request

_app.py_
{% highlight python %}
from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def print_env():
        return os.environ['MY_KEY']

if __name__ == '__main__':
     app.run()
{% endhighlight %}

_requirements.txt_
{% highlight ini %}
appdirs==1.4.3
click==6.7
Flask==0.12.1
itsdangerous==0.24
Jinja2==2.9.6
MarkupSafe==1.0
packaging==16.8
pyparsing==2.2.0
six==1.10.0
Werkzeug==0.12.1
{% endhighlight %}

In the following two videos you will see how changing the value on consul will result into our sample application to get restarted, reading the new environmental variable values

<div id="asciicast-container-4kqzet47wtl3feljz7utvqhhb" class="asciicast" style="display: block; float: left; overflow: hidden; padding: 0px; margin: 20px 0px;"><iframe src="https://asciinema.org/api/asciicasts/1jsu9qgicp29w9bdvgm02fvi3?size=small&amp;autoplay=true&amp;loop=true" id="asciicast-iframe-4kqzet47wtl3feljz7utvqhhb" name="asciicast-iframe-4kqzet47wtl3feljz7utvqhhb" scrolling="no" allowfullscreen="true" style="overflow: hidden; margin: 0px; border: 0px none; display: inline-block; width: 576px; float: none; visibility: visible; height: 468px;"></iframe></div>



<div id="asciicast-container-4kqzet47wtl3feljz7utvqhhb" class="asciicast" style="display: block; float: none; overflow: hidden; padding: 10px; margin: 20px 0px;"><iframe src="https://asciinema.org/api/asciicasts/7swiqyh85qrg1he29dekyeo45?size=small&amp;autoplay=true&amp;loop=true" id="asciicast-iframe-4kqzet47wtl3feljz7utvqhhb" name="asciicast-iframe-4kqzet47wtl3feljz7utvqhhb" scrolling="no" allowfullscreen="true" style="overflow: hidden; margin: 0px; border: 0px none; display: inline-block; width: 576px; float: none; visibility: visible; height: 468px;"></iframe></div>

## Using it with Docker
So, what is left is using it inside Docker (or moby now :/)
Well you can use it in many ways


{% highlight %}
FROM python:2.7-alpine
ADD envconsul /usr/bin
ADD app.py /app.py
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ENTRYPOINT ["envconsul","-consul", "myconsulserver.example.com","-prefix","/"]
CMD ["python","/app.py"]

{% endhighlight %}

OR.


{% highlight %}
FROM python:2.7-alpine
RUN wget https://releases.hashicorp.com/envconsul/0.6.1/envconsul_0.6.1_linux_amd64.zip&&unzip envconsul_0.6.1_linux_amd64.zip\
&& ln -sf $PWD/envconsul /usr/local/bin
ADD app.py /app.py
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ENTRYPOINT ["envconsul","-consul", "myconsulserver.example.com","-prefix","/"]
CMD ["python","/app.py"]

{% endhighlight %}


OR.

{% highlight %}

FROM python:2.7-alpine
RUN wget https://releases.hashicorp.com/envconsul/0.6.1/envconsul_0.6.1_linux_amd64.zip&&unzip envconsul_0.6.1_linux_amd64.zip\
&& ln -sf $PWD/envconsul /usr/local/bin
ADD app.py /app.py
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ENTRYPOINT envconsul -consul 172.17.0.2:8500 -prefix $PREFIX python /app.py

{% endhighlight %}

and then you can pass the prefix in the runtime `docker run -e "PREFIX=/ myimage`

You know you get the picture you can manipulate your Dockerfile any way you want to use envconsul

## env2consul
It's a small utility that will act as a webhook to your github repo holding your env files, and will automatically sync the changes you do on the repo to your consul server
To have a better way to maintain your env and tracking the changes to it

[https://github.com/aabed/env2consul](https://github.com/aabed/env2consul)

<div id="fb-root"></div>
<script>(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.9";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));</script>

<style media="screen" type="text/css">
        .fb_iframe_widget span
        {
            vertical-align: baseline !important;
        }
        </style>
<br>
<p>
<div class="fb-share-button" data-href="https://developers.facebook.com/docs/plugins/" data-layout="button" data-size="small" data-mobile-iframe="true"><a class="fb-xfbml-parse-ignore" target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdevelopers.facebook.com%2Fdocs%2Fplugins%2F&amp;src=sdkpreparse">Share</a></div>

<script src="//platform.linkedin.com/in.js" type="text/javascript"> lang: en_US</script>
<script type="IN/Share"></script>

<a href="https://twitter.com/share" class="twitter-share-button" data-show-count="false">Tweet</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
</p>
