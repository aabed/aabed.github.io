---
layout: post
title: "Building docker images for sbt multi module projects"
description: "Dockerize sbt multi-module project using sbt native packager"
category:
tags: ["sbt","scala","docker","multi-module","sbt-native-packager"]
---
{% seo %}
{% include JB/setup %}
<br>
I don't why but seems like sbt multi-module is a good thing :), so I got a lot of those projects which I need to create docker images for to deploy into production

So here is how to create docker images for those multi-module projects

let's clone the sample repo for this post
Since I don't know scala I asked my beautiful wife to write this sample project, thanks honey (https://twitter.com/MennaEssa)
<br>
{% highlight bash %}
git clone https://github.com/aabed/sbt-multi-module-project-sample.git
{% endhighlight %}
<br>

#### Installing sbt native packager

first you will need to install sbt-native-packager plugin so that we can create docker images

so in **project/plugins.sbt** add this line
{% highlight scala %}
addSbtPlugin("com.typesafe.sbt" % "sbt-native-packager" % "1.2.0-M8")
{% endhighlight %}

#### Enable docker packager for each module
We need to enable docker-plugin to create docker images but this will not work without enabling java-app-packaging because if we did not nothing will get packaged and you might get this error

``` [error] opt: no such file or directory ```

You can enable only the docker plugin if you are going to use it to stage the images i.e ``` sbt docker:stage ```


**build.sbt**
{% highlight scala %}
lazy val sample1 = project.in(file("sample1")).
enablePlugins(JavaAppPackaging).
enablePlugins(DockerPlugin)
{% endhighlight %}

#### Creating docker images for the submodules
<br>

##### Building all submodules

{% highlight scala %}
sbt docker:publishLocal
{% endhighlight %}
<br>

##### Building a specific submodule

{% highlight scala %}
sbt sample1/docker:publishLocal
{% endhighlight %}
<br>

#### More options

Let's do a few tweaks to our image for sample1

{% highlight scala %}
lazy val sample1 = project.in(file("sample1")).
enablePlugins(JavaAppPackaging).
enablePlugins(DockerPlugin).
settings (
  daemonUser in Docker := "root",
  packageName in Docker := "hello-world-1",
  dockerUpdateLatest := true,
  dockerBaseImage:= "java"
)
{% endhighlight %}

<br>

### Further readings

* [sbt native packager](http://www.scala-sbt.org/sbt-native-packager/formats/docker.html)
* [sbt reference manual](http://www.scala-sbt.org/0.13/docs/Basic-Def.html)

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
