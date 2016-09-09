---
layout: post
title: "Resize Linux VM disk on Azure"
description: ""
category:
tags: ["Azure"]
---
{% include JB/setup %}
# How to resize a Linux VM disk on Azure


 * Log in to your panel on Azure
 * Select the machine you want to expand the hard disk for

 ![alt text](https://github.com/aabed/aabed.github.io/raw/master/imgs/azure_1.png)

 * Shut it down

 ![alt text](https://github.com/aabed/aabed.github.io/raw/master/imgs/azure_3.png)

 * Select the disk settings from the right panel

 ![alt text](https://github.com/aabed/aabed.github.io/raw/master/imgs/azure_2.png)

 * Select the disk you want to expand

 ![alt text](https://github.com/aabed/aabed.github.io/raw/master/imgs/azure_4.png)


 * Resize it and click save
 * Now start the machine back again
 * Login to the machine
 * Use fdisk to expand the disk

 ![alt text](https://github.com/aabed/aabed.github.io/raw/master/imgs/azure_5.png)

The disk name may differ on you machine

 * After the reboot you may need to run

 ```
 resiz2fs /dev/sda1
 ```
