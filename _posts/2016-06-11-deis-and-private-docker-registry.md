---
layout: post
title: "Deis and private Docker registry"
description: ""
category:
tags: ["deis","docker","registry","paas"]
---
{% include JB/setup %}
# Deis

Deis is an open source PaaS that leverages Docker, CoreOS and Heroku Buildpacks to provide a private application platform that is lightweight and flexible.

We use it for developers to push and share their work together, However at some point it stopped working

After investigating a little bit I realized that I've just changed our Docker registry to be a private one

Here is the solution as they are not supporting private registery in Deis version1

# Deis Builder

Builder creates Docker images to be run elsewhere on the Deis platform. Builder itself also runs in a Docker container. so we are going to patch the builder Docker image to contain our login credentials

On every node of your Deis cluster do the following

```sh
docker run -it --privileged=true deis/builder:<version> /bin/sh
docker login <your credentials and address>
```

Without closing the shell in the container, commit your changes overriding the current image of deis/registry

```sh
docker commit <container id> deis/builder:<version>
```
and here you go your builders can now pull private images from your registry
Whenever you feel like upgrading the builder image just pull the latest and patch it



# Links:

 * [Deis](http://deis.io)
 * [https://github.com/deis/deis/issues/2232](https://github.com/deis/deis/issues/2232#issuecomment-215123091)
 * [https://github.com/deis/deis/tree/master/builder](https://github.com/deis/deis/tree/master/builder)
