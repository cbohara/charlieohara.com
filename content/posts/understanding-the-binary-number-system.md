---
title: "Understanding the Power of Binary"
date: 2016-06-01
excerpt: "I am grateful I picked up a copy of Code: The Hidden Language of Computer Hardware and Software by Charles Petzold after hearing a shoutout…"
medium: https://medium.com/@cbohara/understanding-the-binary-number-system-45e5fb795b1e
---

I am grateful I picked up a copy of [*Code: The Hidden Language of Computer Hardware and Software*](https://www.amazon.com/Code-Language-Computer-Developer-Practices-ebook/dp/B00JDMPOK2?ie=UTF8&btkr=1&ref_=dp-kindle-redirect) by Charles Petzold after hearing a shoutout for it on [CodeNewbie](http://www.codenewbie.org/). It is very accessible and incredibly interesting for all sorts of folks, but I think it is especially useful for people taking alternative means to learn computer programming beyond the traditional computer science degree route. I am only halfway through and have learned so much about ***why*** we write code the way we write code. I plan on writing of few blog posts summarizing this book so hopefully you will be enticed to go get a copy for yourself.

Petzold introduces us to the concept of code by explaining how two young kids living across the street from one another could communicate after their bedtimes with just their flashlights. They could correspond each blink of light to a letter of the alphabet (e.g. one blink for A, two blinks for B). In reality this quick fix would take forever. A much more efficient option would be to use Morse code. All it takes to communicate every letter in the alphabet is a quick blink of light (“dot”) and a longer blink of light (“dash”). While we do not use Morse code with computers, it is incredible that the entire alphabet can be communicated with just ***two*** types of blinks- quick and long!

![](/img/medium/understanding-the-binary-number-system-1.png)

How is this possible? Well, if we want to share the name of our favorite movie to our friend, we could simply flash a quick “dot” and a longer “dash” for “ET”. And if we wanted to let our friend know the most important character in our favorite book, we would flash “dash dash” “dot dash” “dot dot” “dash dot” to communicate the “MAIN” character. Did you notice that 1 dot or dash can code for 2 letters yet a combo of 2 dots and/or dashes can code for 4? If we kept going, we could use 3 dots and/or dashes to code for 8 more letters. Noticing a pattern? Finally we could use 4 dots and/or dashes to code for 16 more letters. Now that we have 2 + 4 + 8 + 16 = 32 possible letter codes, we have enough for the 26 letters of the alphabet. Simply put, we were able to double the number of letter codes each time we added a dot and/or dash to our combo. Here is a table to help the visual learners like myself:

![](/img/medium/understanding-the-binary-number-system-2.png)

As you may guess, this is a very helpful introduction to binary code, which is simply defined as code that consists of only 2 options. Dot or dash. 0 or 1. Petzold notes the funny observation that humans are likely so attached to the decimal number system because we have 10 fingers. Let’s break down this comfort with the decimal number system so we can easily grasp the binary number system. Take the decimal number 255 and break it down into:

**255 = 200 + 50 + 5**

**255 = (2 x 100) + (5 x 10) + (5 x 1)**

**255 = (2 x 10²) + (5 x 10¹) + (5 x 10⁰)**

The middle line may look most familiar because as kids we were taught that there is a ones place, a tens place, a hundreds place, etc. The last line is just another way of noting that each digit position corresponds to a power of 10. For binary number systems the only difference is each digit position corresponds to a power of 2. The decimal number 255 is equivalent to the binary number 11111111. One thing to note about binary is we often use a space or dash between groupings of four binary digits because it’s easier to read 1111 1111 or 1111–11111. Using the same steps as earlier let’s break down 1111–1111.

**1111–1111 = 1000–0000 + 0100–0000 + 0010–0000 + 0001–0000 + 0000–1000 + 0000–0100 + 0000–0010 + 0000–0001**

**1111–1111 = (1 x 128) + (1 x 64) + (1 x 32) + (1 x 16) + (1 x 8) + (1 x 4) + (1 x 2) + (1 x 1)**

**1111–1111 = (1 x 2⁷) + (1 x 2⁶) + (1 x 2⁵) + (1 x 2⁴) + (1 x 2³) + (1 x 2²) + (1 x 2¹) + (1 x 2⁰)**

Instead of the more familiar ones place, tens place, hundreds place, etc., we now have a ones place, a twos place, a fours place, etc. Each binary digit corresponds with a power of 2. Binary may seem confusing to wrap your mind around at first, but there is huge power in being able to communicate with only two options (0 or 1). So let’s use another tool we learned as kids to help us get more familiar with binary- counting! Now let’s image we have two flippers rather then ten fingers while we count, and image we are a super smart computer science dolphin that likes to start counting from 0 because that is the convention. So let’s count left fin 0, right fin 1, left fin… we can’t do two because we don’t even know what two is. So we say jump over to the twos place with 10. Now back to the right fin for 11, now back to the left fin… again we only have 0s or 1s, so now we jump to the fours place with 100. Now the right fin is 101, left fin is 110, right fin is 111, left fin is… now we jump over to the eights place with 1000. And we can keep going as shown in the table below.

![](/img/medium/understanding-the-binary-number-system-3.png)

Note that we often write binary with leading zeros (e.g. 0001 instead of 1)

Now that we have a better understanding of how the binary number system works, how can we put this to good use? Well, the beauty of utilizing the simplest number system possible is each *bit* (short for binary digit) “has come to be regarded as *the basic building block of information*” so while “a bit represents the smallest amount of information possible, more complex information can be conveyed with multiple bits.” Most people have a very, very abstract understanding that in computer programming everything can be communicated with 0s and 1s. The great thing about reading *Code* is I am learning how “*any information that can be reduced to a choice among two or more possibilities can be expressed using bits*.”

Petzold helps turn this abstract idea into reality with the use of movie reviews. The famous two thumbs up system provided by the late film critics Roger Ebert and Gene Siskel can be transformed into two bits of information. Earlier I noted that with a binary number system, two bits of information can lead to four possible outcomes because 2²= 4. In the example below, the first bit represents Siskel’s review and the second bit represents Ebert’s review. Conventionally “we like to think of 1 bit as representing something affirmative and 0 bit as the opposite,” so 1 is thumbs up and 0 is thumbs down.

![](/img/medium/understanding-the-binary-number-system-4.png)

Now what if I wanted to add my own opinion into the mix? Adding a third bit of information will now produce 8 different possibilities because 2³= 8.

![](/img/medium/understanding-the-binary-number-system-5.png)

How cool is that? We can now communicate more complex ideas with just 0s and 1s. Bits are the building blocks that allow us to communicate with a computer via code.
