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

**Locate the Cloud secion in order to configure docker**

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-3.png" width="100%">

to enable docker api interface on your host enable
edit your /etc/init/docker or /etc/init/docker.io.conf based on your installation
<br>and update the DOCKER_OPTS variable to the following

```DOCKER_OPTS='-H tcp://0.0.0.0:4243 -H unix:///var/run/docker.sock'```

**Now let's locate the Sbt section and configure your sbt installation**

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-4.png" width="100%">

<br>

# Jenkins Jobs

<br>

## Starting Cassandra Docker for our application for testing

As you can guess from our app's name it uses Cassandra database so we need to start a Cassandra database container for testing purposes

**Create a new item, name it and chose Freestyle project**

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-5.png" width="100%">

**Add build step and chose Start/Stop Docker Containers**

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-10.png" width="100%">

**Configure the docker section to start the container and bind the required ports to the host**

Well you can use some service discovery tools, but come on we are just building a project

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-8.png" width="100%">


**Add build step and chose Execute Shell**

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-10.png" width="100%">

**Sleep 10 seconds waiting for the cassandra to fully boot**

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-9.png" width="100%">

<br>


## TweetActorSpec

**Add our repo**
<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-6.png" width="100%">

**Configure Sbt plugin to run the test**
<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-11.png" width="100%">

<br>

## TweetScannerActorSpec

Let's just copy TweetActorSpec and modify the sbt action

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-12.png" width="100%">

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-13.png" width="100%">

**Repeat the same steps for**

- TweetScanActorIntegrationSpec
- TweetActorsPerformanceSpec

## Tests Job

Let's wrap the tests tasks in a one big task
as we did many times so far start by creating a freestyle job

Now let's run the tests in parallel by typping their names comma separated

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-15.png" width="100%">

<br>

## Main Job

Now let's configure our main job that will trigger all the small jobs for to build

Create a new item, name it and chose Freestyle project

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-5.png" width="100%">


You will be taken to the configuration page
in the **Source Code Management** section
add the repo of the project,chose the branch to build, and you might add credentials if this is a private repo

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-6.png" width="100%">


On the **Build Triggers** section chose
Build when a change is pushed to GitHub

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-7.png" width="100%">


This how you make sure that when a change is accepted and merged in the branch you wish to build the whole process will start

Let's get our main job to trigger ther other tasks and run the tests in parallel

Chose add build step and chose Trigger/call builds on other projects

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-14.png" width="100%">