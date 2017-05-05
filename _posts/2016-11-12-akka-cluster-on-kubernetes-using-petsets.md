---
layout: post
title: "Akka cluster on Kubernetes using petsets "
description: ""
category:
tags: ["Akka","kubernetes","petsets"]
---
{% seo %}
{% include JB/setup %}
Building Akka cluster on Kubernetes using petsets
===================
Setting Akka up in docker is a bit tricky if you tried to make it work with Docker you should've came by
http://blog.michaelhamrah.com/2014/03/running-an-akka-cluster-with-docker-containers/
Also if you tried to get it work with Kubernetes you should've came by
https://github.com/vyshane/klusterd
which uses deployments and services for the nodes to discover the seed nodes with a nice bash script to do so
But with Kubernetes introducing [petsets](http://kubernetes.io/docs/user-guide/petset/) I think there is a better way to use them with Akka

The main problem with Akka in Kubernetes that you can't control the pod states they can restart and get new IPs and Hostnames
Even if you use Kubernetes services you still need to resolve the IPs of the nodes behind it

But this is not the case anymore with the petset

> In Kubernetes, most pod management abstractions group them into disposable units of work that compose a micro service. Replication controllers for example, are designed with a weak guarantee - that there should be N replicas of a particular pod template. The pods are treated as stateless units, if one of them is unhealthy or superseded by a newer version, the system just disposes it.
> A PetSet, in contrast, is a group of stateful pods that require a stronger notion of identity. The document refers to these as “clustered applications”.

Which is what we need for Akka

I will assume you have sbt ready to build the Docker image of your project using the native packager


Project Configuration
-------------
{% highlight java %}
api {
  http {
    hostname = "localhost"
    hostname = ${?HTTP_SERVER_HOSTNAME}
    port = 8888
    port = ${?HTTP_SERVER_PORT}
  }
}

clustering {
  cluster.name = "test-cluster"
  node {
    external-hostname = "127.0.0.1"
    external-hostname = ${?HOSTNAME}${?SERVICE_NAME}
    external-port = 2551
    external-port = ${?NODE_EXTERNAL_PORT}

    internal-hostname = "127.0.0.1"
    internal-hostname = ${?HOSTNAME}${?SERVICE_NAME}
    internal-port = 2551
    internal-port = ${?NODE_INTERNAL_PORT}
  }
  seed {
    hostname = "127.0.0.1"
    hostname = ${?SEED_NODE_HOSTNAME}
    port = 2551
    port = ${?SEED_NODE_PORT}
  }
  seed2 {
    hostname = ${clustering.seed.hostname}
    hostname = ${?SEED2_NODE_HOSTNAME}
    port = ${clustering.seed.port}
    port = ${?SEED2_NODE_PORT}
  }
}

akka {
  actor {
    provider = "akka.cluster.ClusterActorRefProvider"
  }
  remote {
    log-remote-lifecycle-events = off
    netty.tcp {
      hostname = ${?HOSTNAME}
      port = ${clustering.node.external-port}

      bind-hostname = ${?HOSTNAME}
      bind-port = ${clustering.node.internal-port}
    }
  }
  cluster {
    roles = ["frontend", "dependent"]
    seed-nodes = [
      "akka.tcp://"${clustering.cluster.name}"@"${clustering.seed.hostname}":"${clustering.seed.port},
      "akka.tcp://"${clustering.cluster.name}"@"${clustering.seed2.hostname}":"${clustering.seed2.port} ]

    auto-down-unreachable-after = 10s
  }
  http {
    server {
      remote-address-header = on
    }
  }
}

{% endhighlight %}

As per Akka documentation
http://doc.akka.io/docs/akka/2.4.3/scala/remoting.html#Akka_behind_NAT_or_in_a_Docker_container
You need to set hostname and bind-hostname, well this is not a problem anymore because with petset we are sure the the pod will get the same hostname each time, so if it's a seed node there is no chance that it binds to a new hostname which will cause the other nodes to go blind searching for non-existing node
Setting this to HOSTNAME environmental variable is all what we need to get the job done

and as you can see above you can set a static list of seed nodes which will never change even if the pod fails


Petset example
-------------

{% highlight yaml %}

apiVersion: apps/v1alpha1
kind: PetSet
metadata:
  name: ad-http

spec:
  serviceName: "ad-http"
  replicas: 2
  template:
    metadata:
      labels:
        app: ad-http
      annotations:
        pod.alpha.kubernetes.io/initialized: "true"

    spec:
      - name: ad-http
        env:
        -
          name: "DEPLOY_ENV"
          value: "ad-http"
        image: ad-http
        imagePullPolicy: Always
        ports:
        - containerPort: 8888
          name: akka
          protocol: TCP
        - containerPort: 2551
          name: seed
          protocol: TCP

      nodeSelector:
          environment: orkestra

{% endhighlight %}

Don't worry about the `DEPLOY_ENV` variable, we use to point to the prefix of consul where we read the environmental variables from, but this another story

you can add the environmental variables in the manifest like this

```
env:
    - name: SEED_NODE_HOSTNAME
      value: "ad-http-0.ad-http"
    - name: SEED2_NODE_HOSTNAME
      value: "ad-http-1.ad-http"
```


You are good to go now you can replicate the same for any other petsets passing the `SEED_NODE_HOSTNAME` to them and they will happily join the cluster the the seed nodes hostname will always be there
