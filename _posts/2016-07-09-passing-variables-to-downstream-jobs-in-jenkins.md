---
layout: post
title: "Passing Variables to Downstream Jobs In Jenkins"
description: ""
category: 
tags: ["Jenkins","CI/CD","Paramterized Build"]
---
{% include JB/setup %}

# Passing variables between jobs in Jenkins

While working on one of the projects at our company, Developers wrote tests for that project those tests will require to tun against the the specific version of the project that triggered the tests

So if the project is at **build-70** something like this should be running in the project-test job


```
docker run project:build-70 
```
So I wanted to pass the build number from the project to the project tests
Here is how using [Jenkins Parameterized Trigger Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Parameterized+Trigger+Plugin)

1) Go to your upstream job (The job that will trigger the tests), and navigate to **post build actions**

<br />

2) Choose **Trigger paramaterized build on other projects**

![alt text](https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot%20from%202016-07-09%2000-58-47.png)

<br />

3) Click **Add parameter** then choose **Predefined parameters**

![alt text](https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot%20from%202016-07-09%2000-59-35.png)

<br />

4) Write the Parameters in form of **Key=Value**, in my case the value is one of the Jenkins built in variable **BUILD_NUMBER** So **API_BUILD_NUMBER** will be based to the tests job holding the value of **BUILD_NUMBER**

![alt text](https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot%20from%202016-07-09%2000-59-40.png)

<br />

5) Now go to your downstream job (Tests) and use the variable wherever you want, for example in the build script

![alt text](https://raw.githubusercontent.com/aabed/aabed.github.io/master/imgs/Screenshot%20from%202016-07-09%2001-07-14.png)

