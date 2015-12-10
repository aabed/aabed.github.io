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

I will be cutting the process of CI/CD into small jobs, as I was advised during the interview and also based on a small discussion on devopschat

Let's start by provisioning our production environment

## Mesos DNS

Mesos DNS provides dynamic DNS naming for services running on a Mesos cluster, Sounds good for service discovery and that's how I will use it

Go to your cluster node where you want to install mesos-DNS

{% highlight bash %}
sudo yum -y install golang git bind-utils
mkdir ~/go
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
go get github.com/tools/godep
go get github.com/mesosphere/mesos-dns
cd $GOPATH/src/github.com/mesosphere/mesos-dns
godep go build .
{% endhighlight  %}


Modify the config.json to use your zookeeper ip and change the port from 8053 to 53 so it looks like this:
{% highlight json %}

{
  "zk": "zk://192.168.33.10:2181/mesos",
  "masters": ["192.168.33.10:5050"],
  "refreshSeconds": 60,
  "ttl": 60,
  "domain": "mesos",
  "ns": "ns1",
  "port": 53,
  "resolvers": ["8.8.8.8"],
  "timeout": 5,
  "listener": "0.0.0.0",
  "SOAMname": "root.ns1.mesos",
  "SOARname": "ns1.mesos",
  "SOARefresh": 60,
  "SOARetry":   600,
  "SOAExpire":  86400,
  "SOAMinttl": 60,
  "dnson": true,
  "httpon": true,
  "httpport": 8123,
  "externalon": true,
  "recurseon": true
}
{% endhighlight  %}

{% highlight bash %}

cp config.json.sample config.json

{% endhighlight  %}


In the Marathon GUI, create a new launcher named dns
and submit that command into it
don't forget to modify the path to your installation
{% highlight bash %}

sudo /home/vagrant/go/src/github.com/mesosphere/mesos-dns/mesos-dns -v=1 -config=/home/vagrant/go/src/github.com/mesosphere/mesos-dns/config.json
{% endhighlight  %}

<br>


##Cassandra cluster

As the project implies we need Cassandra so we will start a Cassandra cluster and provision it for our first run
I will do that step manually because it's a one time job
replace the IP with your marathon host
this will automatically create the DNS record cassandra.marathon.mesos

***Note***: Modify ``` activator-akka-cassandra/src/main/resources/application.conf ```
to point to whatever cassandra host or cluster you are running

{% highlight bash %}

curl -X POST  http://192.168.33.10:8080/v2/apps/  -H "Content-type: application/json" -d '{
  "id": "cassandra",
  "cpus": 0.5,
  "mem": 256,
"constraints":[[ "hostname","LIKE","node[1-3]" ]],

"ports": [
        7000
    ],

  "instances": 3,
  "container": {
    "type": "DOCKER",
    "docker": {
      "image": "cassandra",
"parameters": [
        { "key": "env", "value": "CASSANDRA_SEEDS=node1,node2,node3" }
      ],

"forcePullImage": true,
      "network": "HOST"
    }
}

}'
{% endhighlight  %}

Provision the Cluster with the required data and create the keyspaces
{% highlight bash %}
cd activator-akka-cassandra/src/data
/opt/apache-cassandra/bin/cqlsh cassandra.marathon.mesos -f keyspaces.cql
/opt/apache-cassandra/bin/cqlsh cassandra.marathon.mesos -f tables.cql -k akkacassandra
/opt/apache-cassandra/bin/cqlsh cassandra.marathon.mesos -f words.cql -k akkacassandra

{% endhighlight %}

<br>

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


## Project's Build job

We will deliver our app in the form of a docker container
So let's first prepare our ``` build.sbt ``` to build out docker container and publish it to our private docker registry
here is the part that we care for in our build.sbt

{% highlight bash %}
maintainer in Docker := "Ahmad Aabed <ahmad.aabed.m@gmail.com>" // The maintainer that will be added to your Dockerfile

dockerRepository := Some("registry.marathon.mesos:5000") // Domain name of your docker registry

dockerUpdateLatest := true // Overriding the latest version with the current build

dockerBaseImage := "java"
{% endhighlight %}

Alright, building this with sbt should be a piece of cake
Create a new freestyle job and add a build step **(Build using sbt)** then configure the sbt section to build and publish the docker image
<br>
<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-21.png" width="100%">

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-22.png" width="100%">
<br>

## Deploying our project's docker image
Create a new job

Add build step (Execurte shell)
Then use marathon API to deploy your new docker to your mesos cluster
{% highlight bash %}
curl -X PUT  http://192.168.33.10:8080/v2/apps/activator  -H "Content-type: application/json" -d  '{
  "id": "activator",
  "cpus": 0.5,
  "mem": 256,
"constraints":[[ "hostname","LIKE","node[2]" ]],


  "instances": 1,
  "container": {
    "type": "DOCKER",
    "docker": {
      "image": "registry.marathon.mesos:5000/activator-akka-cassandra",

"forcePullImage": true,
      "network": "HOST"
    }
},
"upgradeStrategy": {
    "minimumHealthCapacity": 1

    }


}'
{% endhighlight %}


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

Add another build step which will provision the cassandra database with the required tests data

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-16.png" width="100%">

It's all ready for the tests to run

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-17.png" width="100%">

After the tests pass successfully we will build our project artifact which is in this case the a docker container

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-20.png" width="100%">

And finally the job that will deploy our new app image
Choose add post-build action and chose **Build other projects (manual step)** because you know, maybe you don't want to deploy that version right now so it will wait for a manual triger

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-23.png" width="50%">

Then choose the job that will deploy the new docker image

<img src="https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot-18.png" width="100%">



### Links

[https://wiki.jenkins-ci.org/display/JENKINS/Build+Pipeline+Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Build+Pipeline+Plugin)

[https://docs.docker.com/registry/deploying/](https://docs.docker.com/registry/deploying/)

[https://open.mesosphere.com/advanced-course/building-and-running-mesos-dns/](https://open.mesosphere.com/advanced-course/building-and-running-mesos-dns/)

[https://mesosphere.github.io/marathon/docs/deployments.html](https://mesosphere.github.io/marathon/docs/deployments.html)
