---
layout: post
title: "Continuous deployment to Kubernetes using Jenkins"
description: ""
category:
tags: ["kubernetes","jenkins","continuous","deployment"]
---
{% include JB/setup %}
{% seo %}
<br>
Today I want to share how I am deploying to Kubernetes using Jenkins
There are two ways I used to so let's start with the first way

#### Using kubectl in a script step

The first way was to configure `kubectl` on the nodes and then execute it inside a script step in Jenkins
This will require that you install and configure kubectl on each node, if you are using nodes in an "on-demand" style then you'll have to bake it into your images
This also means either you save the configrations under /var/lib/jenkins/.kube/config or wherever your jenkins user's home is, or whatever the user your jenkins slave runs with
or pass the configrations in the command paramaters itself

and then simply call `kubectl` in you build steps

{% highlight groovy %}

node {

    stage('Deploy') {
        sh 'kubectl set image deployment $deploymentName $deploymentName=$imageName:$TAG --record'
    }
}

{% endhighlight %}
<br>
This seems easier when you are running on a single node or you have one or two images for your nodes, but if you have a lot of images and you don't want to bake them again when you change the server's url,credentials or certificate maybe you find the second way more convenient



<br>
#### Using Kubernetes plugin

If you don't want to bake the configurations into your nodes then use Kubernetes plugin
https://wiki.jenkins.io/display/JENKINS/Kubernetes+Plugin

**First** create the credentials in the credentials section in Jenkins

then after you install the plugin

**Jenkins->Manage Jenkins->Configure System**


and then configure you Kubernetes section like the image below

![alt img1](https://github.com/aabed/aabed.github.io/raw/master/imgs/Jenkins_K8S.png)

Then you can use the plugin in the Jenkinsfile as follows

{% highlight groovy %}

node {

    stage('Deploy') {
      wrap([$class: 'KubectlBuildWrapper', caCertificate: '''-----BEGIN CERTIFICATE-----
<<<CERTIFICATE BODY HERE>>>
-----END CERTIFICATE-----''', credentialsId: 'my-kube-creds', serverUrl: 'https://kube.example.com']) {
  sh 'kubectl set image deployment $deploymentName $deploymentName=$imageName:$TAG --record'
    }
}

{% endhighlight %}
<br>
You can ignore the certificate if you checked "Disable https certificate check"

**Note** the `withKubernetes` function is no longer supported you may find references to it in other tutorials or in [Kohsuke Kawaguchi's talk](https://www.youtube.com/watch?v=PFCSSiT-UUQ&t=337s)
but it doesn't work

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
