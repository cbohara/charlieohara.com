---
title: "Demystifying Linked Lists for Ruby Developers"
date: 2016-05-29
excerpt: "Halfway through the Firehose Project(FHP) I decided to pause my program before jumping into the agile team project because I am moving from…"
medium: https://medium.com/@cbohara/what-is-a-linked-list-44a10d63cbae
---

Halfway through the [Firehose Project](https://www.thefirehoseproject.com/)(FHP) I decided to pause my program before jumping into the agile team project because I am moving from northern to southern California. I have decided to make the most out of this pause by pushing myself through [Harvard’s Introduction to Computer Science](https://cs50.harvard.edu/)(CS50) class. This past fall I had watched all the lectures as my first exposure to computer science and, I must admit, it was very challenging to follow along. I can’t emphasize enough how awesome it feels to be working through the course again several months later and to be able to understand most of the lecture content and successfully complete the first [four problem sets](https://github.com/cbohara/HarvardCS50x)!

I am now learning about linked lists in week 5, and I would like to share that linked lists are not as scary as you may think. They are just difficult to understand coming from Ruby land. Someone majoring in computer science would have learn about linked lists while completing their traditional computer science coursework. For example, the first half of CS50 is dedicated to learning the fundamentals of computer programming utilizing the programming language C. C is a low-level programming language, which means the programmer must write very explicit directions in order for the computer to execute a program with very little need for interpretation. Many programmers feel relief when they no longer have to write code in low-level programming languages (e.g. C) and can start writing code in high-level programming languages (e.g. Ruby) because a lot of the tedious details involved with these directions are abstracted away.

> Rubyists are quite lucky since they don’t have to manage the memory themselves. Because developers are lazy and Matz developed his language for people and not machine, memory is managed “magically.” — [Matt Aimonetti](http://merbist.com/2010/07/29/object-allocation-why-you-should-care/)

As you can see in the code snippet below, declaring an array in C looks a lot like declaring an array in Ruby. However, it is important to note that there is a lot less information that the programmer needs to provide when writing code in Ruby as compared to writing code in C. This is because Ruby does not require the programmer to be directive in terms of computer memory allocation. With C, the programmer needs to specify the amount of memory to be allocated for each element of the array. In this example on line 2, I am specifying that each element will be allocated an *int*, or typically 4 *bytes* of memory. It is important to note that in C [an array allocates memory for all its elements lumped together as one block of memory](http://cslibrary.stanford.edu/103/LinkedListBasics.pdf), so the code on line 2 will communicate to the computer that it will need to allocate up to 20 bytes (4 bytes per *int* \* 5 elements) for this array. This is all abstracted away from me when I write code in Ruby.

**`arrays`**

```
// Array in C
int array[5] = {1, 2, 3, 4, 5};

// Array in Ruby 
array = [1, 2, 3, 4, 5]
```

It is also important to note that Ruby does not require the programmer to note the number of elements within the array, whereas C does require this information as indicated by *\[5\]* in line 2 above. This is significant because arrays in C are of *fixed* length, meaning you cannot just add or remove elements from an array after declaring an array in C. Coming from Ruby land, this sounds absurd, because we are often pushing on elements or popping off elements and not realizing how lucky we are to be working with *dynamic* arrays in Ruby. This is not possible with arrays in C because the entire array is given just one single block of memory that cannot be augmented without copying everything over to a new array. C needed to have a dynamic data structure of its own, which is why the linked list exists.

![](/img/medium/what-is-a-linked-list-1.png)

Linked list diagram provided by CS50

You will never be writing code to build linked lists as a Ruby programmer, but it is a helpful to learn about this data structure because it allows you to understand a little more about what is going on, as CS50's professor often says, “underneath the hood” of your computer. While arrays in C are stored as one single block of memory, linked lists are built by “linking” together distinct “nodes” with distinct memory addresses. The list starts with a *head* pointer, which simply allows us to find the first node of the linked list in memory. Each node contains a data value (e.g. *int* *9*) as well as a pointer, which stores the memory address of the next node in the linked list. Because pointers are storing the memory address of each separate node, we can easily add or remove nodes from the linked list.

![](/img/medium/what-is-a-linked-list-2.png)

The pointers given by our sassy friend are hexadecimal memory addresses ([xkcd](https://xkcd.com/138/))

What can make learning linked lists while coding in Ruby especially challenging is most resources available online are writing code in C. While you may attempt to build a linked list in Ruby as in lines 2–9 below, the concept of a pointer is really abstracted away. It may be easier to wrap your head around pointers while working in C so I am going to guide you through lines 12–17.

**`comparison`**

```
// Ruby
class Node
  attr_accessor :data, :pointer
 
  def initialize(data, pointer = nil)
    @data = data
    @pointer = pointer
  end
end

// C
typedef struct node
{
    int data;
    struct node* pointer;
}
node;
```

In line 12 I am defining a *struct*, which is allows me to build a data structure in C, just as defining a class allows me to build objects in Ruby. Line 14 allows for each node to contain a data value (e.g. *int* 9). On line 15 I have the *struct node\* pointer*, the pointer in the current node that will store the next node’s memory address. What may look funny is having *node* in both lines 12 and 17. In C, the *node* on line 17 provides the name of the *struct*, just as in the name of class on line 2 is *Node*. It’s odd the name is at the end but it is what it is. I also had to add *node* on line 12 in order for each node in the linked list to be able to refer to itself or another node.

[![CS50 2015 - Week 5](/img/medium/yt-RsIP1gRneOs.jpg)](https://www.youtube.com/watch?v=RsIP1gRneOs)

*Video: [CS50 2015 - Week 5](https://www.youtube.com/watch?v=RsIP1gRneOs)*

*Update: I have decided to refactor my linked list code at the suggestion of my new programming mentor. My instructions were to reverse a linked list in place using only local variables. I actually found working through the problem this way to really help me understand how linked lists work.*

In the code below, I am using Ruby to build a linked list. First I built a node class (lines 1–20) that contains 2 variables with a handful of getter and setter methods. Variables in Ruby store references to objects, which is another way of saying **variables store memory addresses**. The data variable (line 5) will store a number within a node object. The pointer variable (line 6) will store the memory address of the next node in the list. In the terminal, Ruby will display the entire next node within the pointer variable, but it’s really just pointing to the memory address of the next node in the list.

So the general method to adding a node to the end of the list is to traverse to the end of the current list, create a new node, and update the pointers of the last node to point to the new node (lines 27–37). Then in order to reverse the list, we simply want to **reassign the current node’s pointer to point to the previous node in the list**. First we will need to create the next\_node variable to hold the memory address of the next node in the linked list (line 45). Otherwise the rest of the linked list will be chopped off and forever lost in memory. Then on line 46, we assign (or set) the current node’s pointer to the previous node. Lines 47 and 48 essentially allows me to continue leap frogging down the list. Once I reach then end of the list, I need to make sure I reassign the head variable to the previous node because I need the head node in order to find the linked list in memory.

**`linked_list.rb`**

```ruby
class Node
  attr_reader :data, :pointer

  def initialize(data, pointer = nil)
    @data = data
    @pointer = pointer
  end

  def set_pointer(node)
    @pointer = node
  end

  def get_pointer
    @pointer
  end

  def next?
    !@pointer.nil?
  end
end

class Singly_Linked_List
  def initialize(data)
    @head = Node.new(data, nil)
  end

  def insert_node_at_end(data)
    current_node = @head

    while current_node.next?
      current_node = current_node.get_pointer
    end

    new_node = Node.new(data, nil)

    current_node.set_pointer(new_node)
  end

  def reverse_list
    current_node = @head
    previous_node = nil
    next_node = nil

    while current_node
      next_node = current_node.pointer
      current_node.set_pointer(previous_node)
      previous_node = current_node
      current_node = next_node
    end
    @head = previous_node
  end

  def display
    current_node = @head

    while current_node.next?
      p current_node.data
      current_node = current_node.pointer
    end

    p current_node.data
  end
end

first10 = Singly_Linked_List.new(1)
(2..10).each {|x| first10.insert_node_at_end(x)}
puts "forward!"
first10.display
first10.reverse_list
puts "reverse!"
first10.display
```

I hope this helps demystify linked lists for those working with Ruby and having a difficult time because most resources available for understanding linked lists are written in C. If you are still lost, I’d highly recommend you check out this great video series on YouTube that helped me so much with understanding how linked lists work in memory.

[![Introduction to linked list](/img/medium/yt-NobHlGUjV3g.jpg)](https://www.youtube.com/watch?v=NobHlGUjV3g)

*Video: [Introduction to linked list](https://www.youtube.com/watch?v=NobHlGUjV3g)*

While linked lists may not be helpful as a Ruby developer, getting familiar with this data structure has helped me understand how computers deal with memory allocation, and that is a very important skill for a computer programmer to have! I will now challenge you to build a doubly linked list. And reverse a doubly linked list! Once you understand how to build a singly linked list, a doubly linked list should be easy to implement. In my opinion it’s actually much easier to perform operations on doubly linked lists as compared to singly linked lists. For help, feel free to check out at [my work on linked lists](https://github.com/cbohara/linked_list). Happy coding!
