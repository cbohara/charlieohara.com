---
title: "Docker for Python Developers"
date: 2017-05-12
excerpt: "Last fall I taught myself how to use Docker and wrote a piece titled Docker for Rails Developers . Since then, I have fallen in love with Python and landed a job as a data engineer. At work we are…"
medium: https://medium.com/@cbohara/building-a-flask-rest-api-with-docker-94ca4219f460
---

Last fall I taught myself how to use Docker and wrote a piece titled [Docker for Rails Developers](https://medium.com/@charlie.b.ohara/docker-for-rails-developers-5a2a6c2c0593). Since then, I have fallen in love with Python and landed a job as a data engineer. At work we are building a product that includes a Flask REST API, so I wanted to get more familiar with Flask.

### Big Picture

Understanding the terminology Docker uses may help you understand why the technology exists. “Docker” is another term for a longshoreman, who is the person responsible for loading and unloading cargo ships. Back in the day, this process was incredibly inefficient. It took a huge amount of manpower to carry all the goods on to the ship and then carry all the cargo off the ship.

![](/img/medium/building-a-flask-rest-api-with-docker-1.jpg)

<https://en.wikipedia.org/wiki/Containerization>

The use of shipping containers revolutionized global trade. Transporting goods is now incredibly efficient because shipping containers get loaded and unloaded onto ships with a crane. In a similar spirit, Docker containers provide an efficient way to package and transport our code.

![](/img/medium/building-a-flask-rest-api-with-docker-2.jpg)

<https://commons.wikimedia.org/wiki/File:Cranes_ct4-bhv_hg.jpg>

> “Using Docker, everything required to make a piece of software run is packaged into isolated containers. Unlike VMs, containers do not bundle a full operating system — only libraries and settings required to make the software work are needed. This makes for efficient, lightweight, self-contained systems and guarantees that software will always run the same, regardless of where it’s deployed.” <https://www.docker.com/what-docker>

### Why not just use virtualenv?

If you are Python developer, you are probably familiar with [virtualenv](https://virtualenv.pypa.io/en/stable/). It is a tool used for separating the package dependencies for different applications you are working on. When I run the command **pip3 install Flask**, I am asking the pip3 package manager to add the Flask binary file into the **/usr/local/bin/** directory on my computer. The Flask binary file contains machine code the computer needs to run Flask.

Say you are working on a Flask application, and you know it works with a certain version of Flask. Over time, the maintainers working on Flask may decide to make some changes to the framework that negatively affect your project. If you are not using a virtualenv, and you globally install the latest Flask release by running **pip3 install -U Flask**, your application will no longer work.

To avoid this problem, virtualenv exists. For example, when you create a virtualenv named flask0.12, it will create a directory called **flask0.12** with the directory **flask0.12/bin/** inside of it. When you activate the virtualenv, you will be accessing the binary files in the **flask0.12/bin/** directory, not the global**/usr/local/bin/** directory.

Using virtualenv is great for working on my computer, but what if I want to deploy my Flask application so others can use it? How do I share all my project code as well as all the package dependencies to a web server? This is where Docker can step in and help out.

### Why not just use a virtual machine?

If you are familiar with virtual machines, you may be asking yourself why should I use Docker? I already have experiencing spinning up a virtual machine on my computer using Vagrant, and separating out my projects into different virtual machines. If this is what you are thinking — consider this! Virtual environments take up a lot of space (CPU, RAM, storage) on your computer because each application requires an entire guest operating system. Docker does not.

[![Docker Tutorial - What is Docker & Docker Containers, Images, etc?](/img/medium/yt-pGYAg7TMmp0.jpg)](https://www.youtube.com/watch?v=pGYAg7TMmp0)

*Video: [Docker Tutorial - What is Docker & Docker Containers, Images, etc?](https://www.youtube.com/watch?v=pGYAg7TMmp0)*

A virtual machine (VM) is essentially a computer within a computer. The reason why developers use virtual machines is to make sure that the code environment on their local machine will match the environment that other developers on their team are working in and match the environment of the production server.

How do VMs work? A **hypervisor** is a piece of software, firmware, or hardware that VMs run on top of. The hypervisors themselves run on physical computers, referred to as the **host machine**. The host machine provides the VMs with resources, including RAM and CPU.

The VM that is running on the host machine’s hypervisor is often called a **guest machine**. This guest machine contains both the application and whatever it needs to run that application (e.g. system binaries and libraries). It also carries an entire virtualized hardware stack of its own, including virtualized network adapters, storage, and CPU — which means ***it has its own full-fledged guest operating system***.

Since the VM has a virtual operating system of its own, the hypervisor plays an essential role in providing the VMs with a platform to manage and execute this guest operating system. It allows for host computers to share their resources amongst the virtual machines that are running as guests on top of them.

![](/img/medium/building-a-flask-rest-api-with-docker-3.png)

<https://www.docker.com/what-container>

### Well then how does Docker work?

The one big difference between containers and VMs is that ***containers share the host system’s kernel with other containers***. The **kernel** is a computer program that is the core of a computer’s operating system, with complete control over everything in the system. Therefore, Docker does not require each project have its own its own full-fledged guest operating system.

![](/img/medium/building-a-flask-rest-api-with-docker-4.png)

<https://www.docker.com/what-container>

How does this work? The description above states that “multiple containers can run on the same machine and share the OS kernel with other containers, each running as isolated processes in **user space**.”

What is user space? System memory in Linux can be divided into two distinct regions: **kernel space** and **user space**. Kernel space is where the kernel (the core of the operating system) executes and provides its services. **User space** is that set of memory locations in which user **processes** (executing instance of a program) run.

All user programs (containerized or not) function by manipulating data, but where does this data live? This data is most commonly stored in memory and on disk. The kernel provides an API to these applications via system calls. Example system calls include allocating memory (variables) or opening a file.

![](/img/medium/building-a-flask-rest-api-with-docker-5.png)

<http://rhelblog.redhat.com/2015/07/29/architecting-containers-part-1-user-space-vs-kernel-space/>

When a container is started, a program is loaded into memory from the container image. Once the program in the container is running, it still needs to make system calls into kernel space. ***Essentially containers communicate directly with the kernel of the host operating system***, which is what makes Docker a more resource-efficient option compared to VMs.

### Docker Engine

When we refer to Docker, we are really talking about the Docker Engine, which is the program that creates and runs the Docker container from the Docker image file. It runs natively on Linux systems and is made up of:

- The **Docker Client** is the command line interface (what we communicate with via the terminal).
- A **REST API** which specifies interfaces that programs can use to talk to the daemon and instruct it what to do.
- The **Docker Daemon** runs in the background on the host computer, and it is what actually executes commands sent to the Docker Client — like building, running, and distributing your containers.

![](/img/medium/building-a-flask-rest-api-with-docker-6.png)

<https://docs.docker.com/engine/docker-overview/#docker-engine>

### Download Docker

Curious to try it out for yourself? Well the first thing you need to do is [download Docker for your operating system](https://www.docker.com/community-edition). The Docker documentation has improved quite a bit over the last 6 months, so it should be pretty easy.

Now that you have Docker installed on your computer, let’s get up and running quickly by building a very simple Flask application. The code for this simple Flask application is [**available on github**](https://github.com/cbohara/docker_for_python_developers) to make it easier to follow along.

![](/img/medium/building-a-flask-rest-api-with-docker-7.png)

### Setup Flask App

These are the steps I took in the terminal snapshot above:

- Make a new directory for your project
- Set up a virtual environment in the directory with the command **virtualenv venv**
- Activate the virtual environment with **source venv/bin/activate**
- Make a file **requirements.txt** that has all your dependencies in it. For this simple Flask app, all you need is **Flask==0.11.1**
- Install your dependencies with **pip install -r requirements.txt**
- Make a directory within your project director called **app/**
- Add the code below into**app/main.py**

**`main.py`**

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hey I'm using Docker!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
```

Now that we have our basic Flask app, we can create a Docker image. An image is a lightweight, stand-alone, executable package that includes everything needed to run a piece of software. It is essentially a snapshot of the code and the environment we need to run that code. We will make a Docker image from our **Dockerfile**, so create this file in your project folder and copy and paste the code below.

**`Dockerfile`**

```dockerfile
FROM tiangolo/uwsgi-nginx-flask:flask

COPY ./app /app
```

**FROM** tells Docker what image to pull from the Docker hub repository. We are going to take advantage of this convenient image which has Python, Flask, Nginx, and uWSGI. Nginx is a web server, so it takes care of the HTTP connections and also can serve static files directly and efficiently. uWSGI is the application server that runs your Python code and communicates talks with Nginx.

**COPY** will copy the app/ folder we created on our computer into the Docker container. A container is an actual running instance of a Docker image.

Now that we have a Dockerfile, we can build a Docker image. To do so, we need to be in the root directory of our project in the terminal. Our project filesystem should look like this:

```
docker_for_flask_developers/  
  
  Dockerfile  
  
  requirements.txt  
  
  app/  
    main.py  
  
  venv/
```

So while I am in my docker\_for\_flask\_developers**/** folder, I am going to run the command coto communicate with Docker that it is time to create snapshot of my code and its environment:

![](/img/medium/building-a-flask-rest-api-with-docker-8.png)

This tells Docker to build an image from the **Dockerfile**. Docker will pull down the base image tiangolo/uwsgi-nginx-flask:flask from Docker Hub, then copy our app code into the container.***Important note:*** Every time you change your app code, you need to copy the updated **app/** folder into the container, so you will need to build the image again.

Now that we have created a Docker image, we can finally spin up a Docker container. Enter**docker run -p 80:80 -t simple-flask**in your terminal:

![](/img/medium/building-a-flask-rest-api-with-docker-9.png)

To give our container access to traffic over port 80, we use the -p flag and specify the port on the host that maps to the port inside the container. In our case we want 80 for each, so we include -p 80:80 in our command. If you open up your browser and enter **0.0.0.0:80** (or you can just use **0.0.0.0** since port 80 is the default port for HTTP traffic), you should see your Flask app running in the browser on your computer.

![](/img/medium/building-a-flask-rest-api-with-docker-10.png)

Pretty neat right?! Congrats! You got a Flask application up and running using Docker!
