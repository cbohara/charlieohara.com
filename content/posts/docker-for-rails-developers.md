---
title: "Docker for Rails Developers"
date: 2016-09-15
excerpt: "Intro to Docker"
medium: https://medium.com/@cbohara/docker-for-rails-developers-5a2a6c2c0593
---

> *Step 1: Install Docker and Docker Toolbox*

> *Step 2: Define our Rails Project*

> *Step 3: Create our Rails Project*

> *Step 4: More Efficient Workflow*

> *Step 5: Creating the Database*

> *Step 6: Running the App*

> *Step 7: Proceed as Usual*

> *Quick Summary*

I am very grateful I got turned on to Docker by my mentor. I had been building Ruby on Rails applications using a specific Vagrant development environment provided by the [Firehose Project](https://github.com/kenmazaika/firehose-vagrant/blob/master/mac-online.md) that allowed me to spin up a virtual machine with VirtualBox. The reason why developers use virtual machines is to make sure that the code environment on their local machine will match the code environment that other developers on their team are working in and match the production server.

For example, the Vagrant development environment I was working in was configured to make sure that the [chess web application](https://medium.com/@charlie.b.ohara/building-a-chess-web-application-with-an-agile-development-team-51a25877a6cf#.j4pyzw8mj) I built would work the same on my Macbook as it would on my teammate’s Windows laptop as well as in production on [Heroku](https://team-rook.herokuapp.com/). This worked because we had a Vagrantfile that described the type of machine required for our project and directions on how to configure and provision the machine. This would ensure that our project code would work in any environment that had been provisioned by the Vagrantfile, whether it be on a local machine or in the production server.

Sounds like a great solution! So what are the disadvantages? Anyone new to programming can attest that installing and configuring a new development environment can be time-consuming, tedious, and frustrating. Even when a seasoned developer joins a new company, it can take days to install and configure a new environment on their computer. In addition, traditional development environments take up a lot of space (CPU, RAM, storage) because each application requires an entire guest operating system.

[![Docker Tutorial - What is Docker & Docker Containers, Images, etc?](/img/medium/yt-pGYAg7TMmp0.jpg)](https://www.youtube.com/watch?v=pGYAg7TMmp0)

*Video: [Docker Tutorial - What is Docker & Docker Containers, Images, etc?](https://www.youtube.com/watch?v=pGYAg7TMmp0)*

### Intro to Docker

Docker simplifies the process of building, shipping, and running web application for everyone, not just for DevOps Engineers working for major companies. You can use it in your own development environment and workflow, easily collaborate with other developers, and push your projects up to production in the cloud.

How does Docker work? Docker wraps up the project code with all the information needed to run your application into one self-contained unit known as a container. Fun side note- “docker” is another term for a longshoreman, who is a person employed in a port to load and unload ships. Back in the day, there was no standardized way to load and unload cargo off of ships and the process was very inefficient. Now the shipping industry is incredibly efficient because standard size shipping containers can be easily loaded and unloaded with a crane. Just like shipping containers, Docker containers provide a standardized way to package and transport our applications so that they can efficiently move from one location to another.

If you are like me, you want to learn by doing, so I will explain more as we build a Rails application together. If you want to be seduced into following along and making Docker part of your development reality, read what this fellow blogger had to say…

![](/img/medium/docker-for-rails-developers-1.png)

[https://semaphoreci.com/community/tutorials/dockerizing-a-ruby-on-rails-application](https://semaphoreci.com/community/tutorials/dockerizing-a-ruby-on-rails-application)

Here we go! Let’s build an app!

### Step 1: Install Docker and Docker Toolbox

Docker is a tool that makes it easy for us to build, run, and destroy containers. First you will need to download **Docker for Mac** (or whatever operating system you are using) at the link below.

[Docker](https://www.docker.com/products/docker#/mac)

The “Get Started Tutorial” is super easy to follow. First drag and drop the whale into the Applications folder.

![](/img/medium/docker-for-rails-developers-2.png)

Then double click the **Docker.app** in your Applications folder, and you should see a whale icon appear in your top navigation bar.

![](/img/medium/docker-for-rails-developers-3.png)

I then downloaded the **Docker Toolbox** for my operating system with the link below. (Note: You don’t need to have the Docker Toolbox. For more information on Docker for Mac vs. Docker Toolbox, [check out this link](https://docs.docker.com/docker-for-mac/docker-toolbox/). I found it easier to work with the Toolbox.)

[Docker Toolbox](https://www.docker.com/products/docker-toolbox)

After installation is complete, double click on the Docker folder in your Applications folder. Drag the application labeled **Docker Quickstart Terminal** into your Dock.

![](/img/medium/docker-for-rails-developers-4.png)

Now double click on the **Docker Quickstart Terminal**. You’ll see a cute little whale along with some information our Docker Machine. We will need this IP address later, but will be easy to get by running ***docker-machine ip***.

The first command you will run is:

***docker-machine env default***

![](/img/medium/docker-for-rails-developers-5.png)

We will then be directed to configure our shell by entering the following command in our terminal:

***eval $(docker-machine env default)***

We do this to connect our current operating system with the Docker Machine, which is where we can run commands to control the Docker Engine. Typically when people refer to Docker, they are referring to the Docker Engine, the tool that builds and runs Docker containers.

### Step 2: Define our Rails Project

A Dockerfile is used to create a Docker image. A Docker image is a configuration file that gives instructions on how to run a specific service/program in a particular operating system. The content of a Dockerfile can be as simple as instructions for running Ruby on a Linux machine, and this creates a [Docker image](https://hub.docker.com/_/ruby/). Now a Docker image for running Ruby is pretty useless on its own, but it can be very helpful while building a Docker container.

The Docker image is the template used to build a Docker container. Docker containers provide a basic Linux environment in which images can be ran. A Docker image is composed of a layered filesystem and these files specify the operating system (i.e. Ubuntu), the application framework (i.e. Rails) and all its dependencies, and the application code for our project. Just like a [Ruby class is used as a template for an instance of a Ruby object](https://realworldcoding.io/object-oriented-programming-an-introduction-for-code-newbies-77725ed5e0a4#.fg2gsva72), a Docker image is used to create an instance of a running Docker container. A running Docker container is where our live application exists, just like we can access our live application locally by running ***rails*** ***server*** in the terminal.

Start by creating an empty folder on your Desktop for your Rails application. Drag that folder into your text editor and create a new file called **Dockerfile** (no filename extension at the end). Copy and paste the code below provided by the [Docker Quickstart](https://docs.docker.com/compose/rails/) tutorial into the Dockerfile.

The only mandatory instruction that you need to put into a Dockerfile is called a **FROM** instruction. It lets Docker know what image you'd like your own to be based off. The rest of the instructions allow us to define own Docker image based on the requirements of our specific project.

**`Dockerfile (basic)`**

```
FROM ruby:2.2.0
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev nodejs
RUN mkdir /myapp
WORKDIR /myapp
ADD Gemfile /myapp/Gemfile
ADD Gemfile.lock /myapp/Gemfile.lock
RUN bundle install
ADD . /myapp
```

We need a few more files in our Desktop folder to get started with our Rails project. You will need to create an empty file in the Desktop folder called **Gemfile.lock**. Then create a new file called **Gemfile** and copy and paste the code below into it.

**`Gemfile`**

```ruby
source 'https://rubygems.org'
gem 'rails', '4.2.0'
```

Last but not least, we need to create a file in our Desktop folder called **docker-compose.yml**. When we downloaded the Docker Toolbox, we also downloaded Docker-Compose. It is often the case that we want to have our web application server in one container and our database server in another. Docker-Compose is the awesome tool that allows us to get containers linked up and running together. (Note: Docker-Compose calls running containers services.)

The **docker-compose.yml** below specifies two services:

1. the db (short for database) service will be built according to the pre-made [Postgres Docker image](https://hub.docker.com/_/postgres/)
1. the app (short for application) service will be built according to the **Dockerfile** that exists in our Rails application folder on our Desktop

**`docker-compose.yml (basic)`**

```
version: '2'
services:
  db:
    image: postgres
  app:
    build: .
    command: bundle exec rails s -p 3000 -b '0.0.0.0'
    volumes:
      - .:/myapp
    ports:
      - "3000:3000"
    depends_on:
      - db
```

It is also important to note that in the **docker-compose.yml** file above we are referring to something called volumes. Mounting volumes in development saves a significant amount of time because you don’t have to rebuild the image for every change — Docker temporarily swaps the source directory on the image with the one you have locally. Why is this awesome? Because we don’t need to install anything on our development machine, everything needed to run whatever we want to run is provided by images!

### Step 3: Create our Rails Project

Now that we have these 4 files in our Desktop folder, we can go ahead and run a familiar Rails command to create a new Rails project. Enter the following command in your terminal:

***docker-compose run app rails new . --force --database=postgresql --skip-bundle***

When installing Docker images for the first time, they may take a few minutes to download. The cool thing is that if I want to build another project later that requires the Ruby:2.2.0 image, I won’t have to download it again! If I were working in a traditional Vagrant environment, I would have to provision each virtual machine individually. With Docker, once an image is on my machine, I can use it again and again for other projects. You can see all the images on your machine by typing the command ***docker images*** in your terminal. This is possible because the Docker Engine works on top of my host operating system.

If you peak inside the Desktop folder, you will now see the standard Rails skeleton created after running ***rails new*** in your terminal. Now that we have our Rails application with our Dockerfile in one folder, we will run the following command:

***docker-compose build***

At this point, we are building a custom Docker image for our project based on the Dockerfile in our Desktop folder.

### **Step 4: More Efficient Workflow**

You may be wondering how this is any faster than your usual Rails workflow. It takes a really long time to install all the dependencies for our project. Getting started with Docker has a steep learning curve, but you are about to hit a nice sweet spot of productivity and joy!

We can make changes to our Dockerfile and docker-compose.yml file in order to minimize the amount of time it takes to run bundle install and get our application and database running together.

First copy and paste the file below into your own **Dockerfile**. The advantage of this updated Dockerfile is it uses the Ruby Alpine Docker image. Ruby Alpine is built with Alpine Linux, a very small Linux distribution that only contains the minimum files needed to run the Linux operating system. This Dockerfile is also better because I won’t need to wait to install every gem every time I run ***bundle install,*** which allows my workflow with Docker to be even more efficient.

**`Dockerfile`**

```dockerfile
FROM ruby:2.3-alpine

# Set all environment variables at once
ENV GOSU_VERSION=1.9 \
    GEM_HOME=/home/app/bundle \
    BUNDLE_PATH=/home/app/bundle \
    BUNDLE_APP_CONFIG=/home/app/bundle \
    APP=/home/app/webapp \
    PATH=/home/app/webapp/bin:/home/app/bundle/bin:$PATH \
    DB_ADAPTER=sqlite3

# Install bash, less, nodejs, db clients and gosu
# Create app directory and set permissions
# Remove cache
RUN apk add --no-cache \
    bash less nodejs \
    build-base ruby-dev \
    libc-dev libffi-dev \
    sqlite-dev postgresql-dev mysql-dev \
    libxml2-dev libxslt-dev \
    tzdata \
    dpkg gnupg openssl \
 && dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
 && wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch" \
 && wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc" \
 && export GNUPGHOME="$(mktemp -d)" \
 && gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 \
 && gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu \
 && rm -r "$GNUPGHOME" /usr/local/bin/gosu.asc \
 && chmod +x /usr/local/bin/gosu \
 && gosu nobody true \
 && addgroup -g 1000 app \
 && adduser -u 1000 -D -G app -s /bin/bash app \
 && mkdir -p "$APP" "$GEM_HOME/bin" \
 && { \
    echo 'install: --no-document'; \
    echo 'update: --no-document'; \
  } >> /home/app/.gemrc \
 && chown -R app:app /home/app \
 && find / -type f -iname '*.apk-new' -delete \
 && rm -rf '/var/cache/apk/*' '/tmp/*' '/var/tmp/*'

WORKDIR $APP
COPY start.sh template.rb entrypoint.sh install_rails.sh /home/app/

ENTRYPOINT ["/home/app/entrypoint.sh"]
CMD ["/home/app/start.sh"]
```

Now copy and paste the code below into your **docker-compose.yml** file.

**`docker-compose.yml`**

```yaml
version: '2'
services:
  app:
    image: nooulaif/rails:latest
    environment:
      - RAILS_VERSION=4.2.0
      - APP_NAME=example
      - DB_HOST=db
      - DB_ADAPTER=postgresql
      - DB_USER=postgres
    volumes:
      - ./:/home/app/webapp
      - bundle_data:/home/app/bundle
    depends_on:
      - db
    ports:
      - 3000:3000
  db:
    image: postgres:9.5
    volumes:
      - db_data:/var/lib/postgresql
    logging:
      driver: none
volumes:
  bundle_data:
    driver: local
  db_data:
    driver: local
```

Now run ***docker-compose build*** to create a new Docker image from our **docker-compose.yml**.

### Step 5: Creating the Database

We need to set up our database connections in our **config/database.yml** file so copy and paste the code below.

**`database.yml`**

```yaml
default: &default
  adapter: postgresql
  encoding: unicode
  pool: 5
  timeout: 5000
  username: postgres
  port: 5432
  host: db

development:
  <<: *default
  host: db

test:
  <<: *default
  host: db
```

The first thing we need to do is create our database. Enter ***docker-compose up -d db*** in the terminal to get the Postgres container running in the background as defined by our db:service in our **docker-compose.yml** file.

Now that we have a running Postgres instance, we can create our development and test databases by running ***docker-compose run --rm app rake db:create***. If all goes well, it should simply return.

### Step 6: Running The App

Finally we can boot the app with ***docker-compose up.*** This is just like running ***rails server*** in our usual workflow. In general I prefer to use the command ***docker-compose up -d*** because the -d tag allows me to continue to use the terminal while the containers are running. We can check on our running containers by entering ***docker ps -a*** in our terminal. This will list all Docker containers, whether or not they are active. If all is well, the status should say the container has been up and running for a certain amount of time.

![](/img/medium/docker-for-rails-developers-6.png)

Now let’s finally see our application! Run ***docker-machine ip*** to get the IP address for the Docker machine. Copy and paste that IP address into your browser, and add the port number we specified in our docker-compose.yml file. For example, my IP address is **192.168.99.100** and the port we are using is **3000**, so I will type in **192.168.99.100:3000** into the browser.

And we finally have arrived!!!!!!!!!!!!!!!!!!!!!

![](/img/medium/docker-for-rails-developers-7.png)

![](/img/medium/docker-for-rails-developers-giphy-5B6MWZsS1iZby.gif)

### **Step 7: Proceed as Usual**

From here you can proceed as you normally would while building a Rails application. After running ***docker-compose up -d***, you can just let your containers continuously run because they utilize so little resources from your machine. You need to add ***docker-compose run app*** in front of your standard Rails commands. Here are a few examples:

***docker-compose run app rails console***

***docker-compose run app rake routes***

***docker-compose run app bundle exec rspec***

When we run ***docker-compose run app bundle install*** or make any changes to our configuration files, we are going to want to restart our server as we normally would. This can be done by using ***docker restart***.

After running the command

***docker-compose run app bundle install***

then run

***docker ps -a***

to get the name of the container that you want to restart. The run

***docker restart \[container\_name\]***

Otherwise you should be good to go!

### **Quick Summary**

We went through a ton of material, so I just want to add a quick review before I wrap things up.

- We build a custom Docker image based on the Dockerfile.
- We spin up a Docker container based on the Docker image.
- We use Docker-Compose to spin up and connect multiple containers as directed in the docker-compose.yml file.
- We continue to use Docker-Compose to run standard Rails commands.

If you want to check out my demo project, check out the repo at [https://github.com/cbohara/docker\_for\_rails\_developers](https://github.com/cbohara/docker_for_rails_developers).
