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

## Installing jenkins plugins
![]("../imgs/Screenshot-1.png")

## Main Job
