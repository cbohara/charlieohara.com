---
title: "Recursion Revealed!"
date: 2016-09-30
excerpt: "Recursion finally clicked for me after watching this video:"
medium: https://medium.com/@cbohara/recursion-revealed-f8543e4dad1c
---

Recursion finally clicked for me after watching this video:

[![Data Structures Using C++: Illustration of Recursive Function Calls (Call Stack)](/img/medium/yt-k0bb7UYy0pY.jpg)](https://www.youtube.com/watch?v=k0bb7UYy0pY)

*Video: [Data Structures Using C++: Illustration of Recursive Function Calls (Call Stack)](https://www.youtube.com/watch?v=k0bb7UYy0pY)*

I fear some may not watch it because the instructor is using C++, but he does such an excellent job explaining how recursion works that I thought I’d take a few minutes to explain recursion to those of us using very high-level programming languages such as Ruby.

Take the classic factorial problem. You may remember having to calculate the factorial of a number back in school. For example, the factorial of 5 is:

### 5! = 5 \* 4 \* 3 \* 2 \* 1 = 120

We can certainly take an iterative approach to this problem. [It is important to note that **0! = 1**](https://www.khanacademy.org/math/precalculus/prob-comb/combinatorics-precalc/v/zero-factorial-or-0). If we call **factorial(0)** below, then our function will return **1**. If we call **factorial(5)**, then we will use a for loop starting on line 4 to iterate from 1 to n = 5.

**`iterative_factorial.rb`**

```ruby
def factorial(n)
  return 1 if n == 0
  result = 1
  for i in 1..n
    result = result * i
  end 
  return result
end

factorial(5)
```

This is what an iterative approach looks like step-by-step:

![](/img/medium/recursion-revealed-1.jpg)

While you are better off taking an iterative approach to this problem, and I will explain more why later, sometimes it is easier to work through algorithmic challenges using **recursion**.

Why? Sometimes a problem is too difficult or too complex to solve on its own, but it can be broken down into smaller versions of itself that are solvable. A recursive approach allows us to break down a problem into smaller pieces that you either already know the answer to or can solve by applying the same algorithm to each piece and then combining the results. The smallest version of the algorithm that is solvable is the **base case**.

Now we will approach the factorial problem using recursion. The first question we need to ask is ***what is our base case?*** I think what most threw me off about recursion is thinking I am done solving the problem once I reach the base case. Not true! Reaching the base case means we can ***stop making recursive calls to the function***, but all the pieces of the puzzle need to be put together to form the final answer.

We need to be able to stop making recursive calls to the function and reach the base case, so it is critical to set up your algorithm so each recursive function makes progress towards the base case. Otherwise we will experience infinite recursion (a special case of an infinite loop), and get the infamous stack overflow error.

For the factorial problem, the smallest possible value of n is **0**. That means our **base case** is **factorial(0) = 1**. In the code below, we set up our base case on lines 2 and 3 to ensure that if we reach our base case, when n equals 0, then we will not make another call to the factorial function.

**`factorial.rb`**

```ruby
def factorial(n)
  if n == 0
    return 1
  else
    return n * factorial(n-1)
  end
end

factorial(5)
```

In the code above we call the function **factorial(5)** on line 9. We will then skip to line 1 to start executing our function with n = 5. We will bypass the if statement and jump down to line 5, which tells the computer to return **n \* factorial(n-1)**. This demonstrates how to set up our algorithm so that we progress towards the base case, which is when n equals 0. But what does it mean to return **n \* factorial(n-1)**, or in this instance **5 \* factorial(4)**?

Let’s take a step back and understand what is happening in memory when we call a function. Our computer uses a data structure called [a stack](https://en.wikipedia.org/wiki/Stack-based_memory_allocation), which you can image just like a stack of trays.

![](/img/medium/recursion-revealed-2.png)

<https://study.cs50.net/stacks>

It would be pretty ridiculous if you tried to grab a tray from the bottom of one these stacks. Doesn’t it make much more sense to grab the tray on top? This is how stacks work in memory. Stacks are considered a Last In — First Out(LIFO) data structure because we can only push elements on top of the stack and pop elements off the top of the stack.

![](/img/medium/recursion-revealed-3.jpg)

<https://www.tutorialspoint.com/data_structures_algorithms/stack_algorithm.htm>

What does this have to do with recursion? Well it is important to realize what happens in memory when we make a function call. The computer is able to keep track of the active functions in a program by using a [call stack](https://en.wikipedia.org/wiki/Call_stack). “Active” functions are those that have been called but not yet returned. (A return statement stops the execution of a function.)

Each time a function is called, an activation record is created and put on top of the call stack. This activation record contains the function’s parameters, the function’s local variables, and a return address to indicate where in the code to start executing once this specific function is done. Once the function returns, then the active record is popped off the stack, and we are sent back to code where the return address specified.

This is all very abstract, so I will walk through how the call stack works with the factorial function. This is where I hope enlightenment will occur.

**`factorial.rb`**

```ruby
def factorial(n)
  if n == 0
    return 1
  else
    return n * factorial(n-1)
  end
end

factorial(5)
```

We call the function **factorial(5)** on line 9. This will create the first activation record in our call stack.

![](/img/medium/recursion-revealed-4.jpg)

We jump to line 1 and skip down to line 5, which returns **5 \* factorial(4)**. This will be the second activation record placed on the stack.

![](/img/medium/recursion-revealed-5.jpg)

Since part of the return includes a recursive function call, we need to execute **factorial(4)**. This simply means we jump back to line 1 and then down to line 5, which returns **4 \* factorial(3)**. We have made another function call with **factorial(3)**, so we need to add an activation record on top of our call stack.

![](/img/medium/recursion-revealed-6.jpg)

Returning **factorial(3)** means we jump back to line 1, jump down to line 5, and return **3 \* factorial(2)**, and add another activation record to our call stack. We will keep repeating this process until we finally reach our **base case**, when n equals 0. When we have reached our base case, we will no longer be making recursive calls to the factorial function.

![](/img/medium/recursion-revealed-7.jpg)

So where do we go from here? Well let’s look back at our function. We know that the **factorial(0) = 1**, which is what is returned once we reach our base case on line 3.

**`factorial.rb`**

```ruby
def factorial(n)
  if n == 0
    return 1
  else
    return n * factorial(n-1)
  end
end

factorial(5)
```

Therefore, the value of **1** is returned when **factorial(0)** is called, and the top activation record is popped off the call stack. Where does the value 1 get returned? It gets returned the the function that called **factorial(0)**.

![](/img/medium/recursion-revealed-8.jpg)

Now that we have solved for **factorial(1) = 1 \* 1 = 1**, we can pass this value into the next statement to be solved, and pop off the top activation record off the call stack.

![](/img/medium/recursion-revealed-9.jpg)

Now we can solve **factorial(2) = 2 \* factorial(1) = 2 \* 1 = 2**, pass **factorial(2) = 2** into the next statement to be solved, and pop this activation record off the top of the stack.

![](/img/medium/recursion-revealed-10.jpg)

Now we can solve **factorial(3) = 3 \* factorial(2) = 3 \* 2 = 6**, pass **factorial(3) = 6** into the next statement to be solved, and pop this activation record off the top of the stack.

![](/img/medium/recursion-revealed-11.jpg)

Now we can solve **factorial(4) = 4 \* factorial(3) = 4 \* 6 = 24**, pass **factorial(4) = 24** into the next statement to be solved, and pop this activation record off the top of the stack. We are almost there!

![](/img/medium/recursion-revealed-12.jpg)

Now we can finally solve **factorial(5) = 5 \* factorial(4) = 5 \* 24 = 120**.

![](/img/medium/recursion-revealed-13.jpg)

Looking back at our original code, after all those recursive calls, we will finally return **factorial(5)** **= 120** on line 9.

**`factorial.rb`**

```ruby
def factorial(n)
  if n == 0
    return 1
  else
    return n * factorial(n-1)
  end
end

factorial(5)
```

You may be wondering why we went through all this trouble to solve the factorial problem. And that is a very good question! In this case, it would make more sense to use an iterative approach because it consumes fewer resources in terms of time and memory.

So then why deal with recursion at all? People use recursion when it is very complex to write an iterative solution to an algorithm. And there are times when it is worth taking a recursive approach because it is more time efficient compared to an iterative approach. For example, many classic computer science problems involve sorting an unordered list of numbers in an array. While an iterative approach such as selection or insertion sort may seem more intuitive, merge and quick sort are much more efficient as the number of elements in the array grows larger and larger.

That’s enough for one post. I hope I offered an accessible yet comprehensive overview of recursion. Be sure to use the [Python Tutor](http://www.pythontutor.com/) tool often (in your language of choice) to better understand how your methods are being called in memory. Happy coding!
