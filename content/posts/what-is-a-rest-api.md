---
title: "What is a REST API?"
date: 2017-05-14
excerpt: "A web API (application programming interface) is an application dedicated to transferring data. Accessing a web API is the same as accessing any other web page via a URL. The difference is APIs…"
medium: https://medium.com/@cbohara/what-is-a-rest-api-79c78de3a6fc
---

A web API (application programming interface) is an application dedicated to transferring data. Accessing a web API is the same as accessing any other web page via a URL. The difference is APIs aren’t easy for people to read. The data returned by an API is formatted for machines.

[![REST API concepts and examples](/img/medium/yt-7YcW25PHnAA.jpg)](https://www.youtube.com/watch?v=7YcW25PHnAA)

*Video: [REST API concepts and examples](https://www.youtube.com/watch?v=7YcW25PHnAA)*

The purpose of an API is to share data from one application to another. Web API data is commonly transferred in the JSON (Javascript Object Notation) format because [“It is easy for humans to read and write” and “It is easy for machines to parse and generate.”](http://www.json.org/)

![](/img/medium/what-is-a-rest-api-1.png)

This is JSON data served by my Catbook Rails 5 API (<https://github.com/cbohara/catbook_API>)

Back in the day, it was a headache to figure out where data was located for different APIs. [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) (representational state transfer) is a standard way to format your API so it is easy for one application to communicate with another. The table below is from the Rails documentation, and it does a great job outlining how RESTful applications should respond to different HTTP requests for different links. If you follow this format, you make it easy for other applications to know where the data in your API is. And the point of a web API is to share data.

![](/img/medium/what-is-a-rest-api-2.png)

<http://guides.rubyonrails.org/routing.html>

I wrote this quick post because it is hard to find a straightforward definition of REST APIs. If you want to learn how to build your own REST API, I would recommend you take the Udemy course [REST APIs with Flask and Python](https://www.udemy.com/rest-api-flask-and-python/learn/v4/overview).
