---
layout: post
title: "Continous Integration/Delivery Using (Jenkins,Docker,Mesos,Marathon.."
description: "Building a CI/CD pipeline for a scala sample project usning different technologies"
category:
tags: ["CI/CD","docker","jenkins","mesos","marathon","devops","continous integration","continous delivery"]
---
{% include JB/setup %}
# The History
A few months ago I got through an interview with a company. I was asked to develop a complete CI/CD pipeline for a sample software.

Well, I failed in the interview, because of a lot of things including not doing the task as it should be,So here I am trying to make things go the right way, after researching and studying

# The tools
- Jenkins
  - sbt plugin
  - build pipeline plugin
  - docker plugin
- Docker/Docker Registry
- Mesos
- Marathon

# The sample project
- https://github.com/aabed/activator-akka-cassandra

# Get down to business

I will be cutting the process of CI/CD into small jobs, as I was adviced during the interview and also based on a small discussion on devopschat

So let's create our jobs

## Installing Jenkins plugins


<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-1.png" width="100%">

Search and install the following plugins

- https://wiki.jenkins-ci.org/display/JENKINS/Docker+Plugin
- https://wiki.jenkins-ci.org/display/JENKINS/sbt+plugin
- https://wiki.jenkins-ci.org/display/JENKINS/Git+Plugin

## Configuring Jenkins

**Open Jenkins configuration page**

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-2.png" width="100%">

**Locate the cloud secion in order to configure docker**

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-3.png" width="100%">

to enable docker api interface on your host enable
edit your /etc/init/docker or /etc/init/docker.io.conf based on your installation
<br>and update the DOCKER_OPTS variable to the following

```DOCKER_OPTS='-H tcp://0.0.0.0:4243 -H unix:///var/run/docker.sock'```


## Main Job
