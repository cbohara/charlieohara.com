---
title: "The Linux Command Line"
date: 2017-02-13
excerpt: "I would consider Docker the most valuable tool in my tool belt as a software engineer. Docker is a tool that packages a software application and its dependencies together in a container so it can…"
medium: https://medium.com/@cbohara/the-linux-command-line-9d6ee43641aa
---

### By William Shotts

### Motivation for learning Linux

I would consider Docker the most valuable tool in my tool belt as a software engineer. Docker is a tool that packages a software application and its dependencies together in a container so it can easily and reliably run on any Linux server.

Well what the heck is a container? A container is a self-contained Linux operating system that shares the kernel of the host operating system. An operating system (OS) is the first piece of software that the computer executes when it is turned on, and the kernel is the central part of an operating system that takes care of managing really important tasks, like managing memory.

The reason why I love using Docker is I do not need to dedicate an entire virtual machine on my personal computer for each project I am working on. Instead I can run multiple containers, which are ultimately lean Linux computers, on my own computer. Therefore in the process of learning how to use Docker, I have inadvertently been learning about the Linux OS.

In a previous post I shared how to use [Docker to build a Rails application](https://medium.com/@charlie.b.ohara/docker-for-rails-developers-5a2a6c2c0593#.nlmmg149s). To deploy this application I could use Amazon’s EC2 Container Service (ECS). I already created a Docker Compose file ([docker-compose.yml](https://github.com/cbohara/docker_for_rails_developers)) in order to coordinate communication between the Rails application and its PostgreSQL database. Using a service like ECS would make it possible to run, stop, and manage my Docker containers “in the cloud.”

Cloud services like AWS allow individuals and companies to no longer worry about setting up their own servers. You may remember the utter failure that the Pied Piper company experienced when trying to set up their own servers in the HBO show *Silicon Valley*.

![](/img/medium/the-linux-command-line-9d6ee43641aa-1.jpg)

<http://www.theregister.co.uk/2015/06/15/silicon_valley_season_2_ep_10/>

![](/img/medium/the-linux-command-line-9d6ee43641aa-2.jpg)

<http://www.theregister.co.uk/2015/06/15/silicon_valley_season_2_ep_10/>

I instead rely on Amazon’s computers, which are running on the Linux operating system, to serve my web application. Essentially each container would be deployed as a Amazon Elastic Compute Cloud (EC2) instance, and an instance is a “virtual server” in the “AWS cloud.”

A virtual server is just sexy way of saying an entire computer is not dedicated to a single server. And the AWS cloud is just referring to a bunch of computers located in an Amazon data center that have software on them that are dedicated to listening to HTTP requests and serving data to the client browser as requested.

![](/img/medium/the-linux-command-line-9d6ee43641aa-3.jpg)

By Victorgrigas — Own work, CC BY-SA 3.0, <https://commons.wikimedia.org/w/index.php?curid=20348454>

Another big buzz word in cloud computing is “elastic,” and this really means that it has become easier for individuals and companies to scale up or down as needed and only pay for only the servers they use.

After I launch an instance, [I can connect to it and use it the way that I would using the computer sitting right in front of me](http://Connecting to Your Linux Instance Using SSH - Amazon Elastic Compute Cloud Connect to your Linux instances using an SSH client.docs.aws.amazon.com). In order to do this though, I need to be comfortable with the Linux OS. Specifically, I need to navigate my application in the cloud by using the command line.

I do not have the option of depending on the graphical user interface (GUI) like I do while working on my Mac OS. However, the nice thing about learning how to use the command line within a Linux OS is many of the commands work the same on my Mac OS. And as William E. Shott’s shared in the introduction of his book, “graphical user interfaces make easy tasks easy, while command line interfaces make difficult tasks possible.”

### The Linux Command Line

The Linux operating system was and continues to be built by a community of people who do not want a few giant corporations to control what they can do with their computer. I believe in this spirit, the writer William E. Shott has made his book *The Linux Command Line* freely available online.

[The Linux Command Line by William E. Shotts, Jr.](http://linuxcommand.org/tlcl.php)

If you are interested in following along the book and have a Mac, I would suggest playing around with running the commands both in your Mac OS terminal as well as in a Linux OS terminal. In order to get a Linux OS running on your Mac computer, you can use VirtualBox. The link below gives very clear instructions on how to do so, and it will only take you a few minutes to get a Linux OS up and running.

[How to Install Ubuntu on Your Mac Using VirtualBox](http://www.simplehelp.net/2015/06/09/how-to-install-ubuntu-on-your-mac/)

I would definitely recommend you read the book yourself! This post will just give you a little taste of the power of the command line, along with some helpful tips and tricks I’ve learned as part of the [San Diego Technology Immersion Group (SDTIG)](https://www.meetup.com/San-Diego-Technology-Immersion-Group-SDTIG/).

### Navigation

When we interact with our operating system using the command line in our terminal, we are really interacting with the shell. The shell is a program that takes keyboard commands and passes them to the operating system to carry out, and most versions of Linux supply a shell program called bash.

One of the first things we can do to start getting familiar with our Linux OS is to navigate the file system. With Linux, everything is a file, and we have the power to know everything about our Linux OS because it is open source software!

If you are already using the terminal on your current OS, you may already be familiar with the commands **pwd**, **cd**, and **ls**. Also, it helps to know that Linux uses the term directory to describe a folder. Directory and folder are the same thing.

**pwd** (print working directory) prints where I currently am in the file system

![](/img/medium/the-linux-command-line-9d6ee43641aa-4.png)

**cd** allows us to change directories (move from one directory to another)

![](/img/medium/the-linux-command-line-9d6ee43641aa-5.png)

**ls** lists the directory’s contents

![](/img/medium/the-linux-command-line-9d6ee43641aa-6.png)

Now is a good time to share a general pattern for commands:

**command -options**

Most commands have options available, which are generally communicated in the command line by using dash followed by a single character. For example, **ls -a** will list all files and directories, even if they are normally hidden because they start with a period.

**ls -a** lists all files and directories

![](/img/medium/the-linux-command-line-9d6ee43641aa-7.png)

**ls -l** displays the list of files in a long format

![](/img/medium/the-linux-command-line-9d6ee43641aa-8.png)

What do all those things mean?!?! Well, this is a helpful table from the book that explains each part.

![](/img/medium/the-linux-command-line-9d6ee43641aa-9.png)

<http://linuxcommand.org/tlcl.php>

### Exploring the System

While **ls -l** is helpful to provide a snapshot of the files in a directory, we now will use the command **file** to return specific information about the file type.

**file *filename***

![](/img/medium/the-linux-command-line-9d6ee43641aa-10.png)

This file can be read using ASCII (American Standard Code for Information Interchange) text. Any information we communicate with our computer needs to be translated into [binary, or 0s and 1s](https://medium.com/@charlie.b.ohara/understanding-the-binary-number-system-45e5fb795b1e#.4lxovri49). ASCII is a very simple 1-to-1 mapping system in which each character is assigned a number. Many files on our Linux OS are ASCII text files, so **less** is a helpful command that allows us to view this text file within our terminal.

> “Why would we want to examine text files? Because many of the files that contain system settings (called *configuration files*) are stored in this format, and being able to read them gives us insight about how the system works. In addition, some of the actual programs that the system uses (called *scripts*) are stored in this format.” -William E. Shott

**less *filename*** allows for the easy viewing of long text documents. Why is the command called **less**? It is play on the phrase “less is more” because **less** is an upgrade on the previous pager **more**. Pagers are simply programs that allow the easy viewing of long text documents in a page by page manner.

Another helpful command is **man** (short for manual), which displays the manual describing how a command works. **man** displays the manual using the less program, so its funny that the **man** command below is using the less program to describe the **less**command.

**man less**

![](/img/medium/the-linux-command-line-9d6ee43641aa-11.png)

In the past, I have used the command **cat *filename*** to display text files in the terminal just like we did earlier with **less**. However, the two commands work a bit differently.

**cat** is short for concatenate, a word that you may have heard of in your programming career. For example, I can use the + sign in Python to concatenate two individual strings into one string, as demonstrated below.

![](/img/medium/the-linux-command-line-9d6ee43641aa-12.png)

**cat** is often used to display short text files, but because **cat** can accept more than one file as an argument, it can also be used to join (or concatenate) files together!

### Manipulating files and directories

Now that we know how to navigate our file system, let’s learn a handful of commands that allow us to directly manipulate files and directories within the terminal without using a GUI! Again, it is powerful to learn how to use the Linux command line because when working with Linux instances deployed “in the cloud,” we do not have access to a GUI.

Four common commands used for manipulating files and directories are **mkdir**, **cp**, **mv**, and**rm**.

![](/img/medium/the-linux-command-line-9d6ee43641aa-13.png)

<http://linuxcommand.org/tlcl.php>

![](/img/medium/the-linux-command-line-9d6ee43641aa-14.png)

<http://linuxcommand.org/tlcl.php>

Here’s an example of how using the **cp** command is more powerful compared to using the GUI. Let’s say I wanted to copy only Python scripts from my current directory to another directory on my Desktop. I can use the wildcard operator **\*** to copy all my Python files in a directory by entering the **cp \*.py** command followed by the directory I would like to copy these files to, which in this case is a directory on my desktop called **testing\_wildcard**.

![](/img/medium/the-linux-command-line-9d6ee43641aa-15.png)

Fair warning though, **cp** will *overwrite existing files of the same name*! It is best practice to use the **-i** (short for interactive) option so you will be told that there is a file of the same name that will be overwritten if you use the **cp** command. If this option is not specified, **cp** will *silently overwrite files*.

![](/img/medium/the-linux-command-line-9d6ee43641aa-16.png)

<http://linuxcommand.org/tlcl.php>

![](/img/medium/the-linux-command-line-9d6ee43641aa-17.png)

<http://linuxcommand.org/tlcl.php>

Just like **cp**, **mv** will *overwrite existing files of the same name*! Again, it is a good idea to use the **-i** (short for interactive) option so you will be told that there is a file of the same name that will be overwritten if you use the **mv**command.

![](/img/medium/the-linux-command-line-9d6ee43641aa-18.png)

<http://linuxcommand.org/tlcl.php>

You may have noticed in your day-to-day while working in the terminal that **rm** can be used to remove (delete) a file from the directory, but cannot be used to delete a directory. In order to delete a directory, you need the use **rm -r *directory***because the **-r** option tells the operating system to [recursively](https://medium.com/@charlie.b.ohara/recursion-revealed-f8543e4dad1c#.ty2yev9qn) delete not only the directory specified but all files and subdirectories within the directory.

Be careful when using **rm**! Once you delete something with **rm**, it is gone. *There is no undelete command.* Just like with **cp** and **mv**, it is a good idea to use **rm -i** so you have one more chance to confirm that you would like the file or directory to be deleted.

### Conclusion

Like I said, this is just a little taste into the magic of Linux. If you want to feel like this [Linux User at Best Buy](https://www.xkcd.com/272/)….

![](/img/medium/the-linux-command-line-9d6ee43641aa-19.png)

Linux User at Best Buy: <https://www.xkcd.com/272/>

… you should start reading [*The Linux Command Line*](http://linuxcommand.org/tlcl.php)!
