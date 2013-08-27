Title: first crack at it
Date: 2011/12/11 22:57
Author: Ken Ko
Tags: reversing, cracking, registration, serial, tutorial, writeup
Category: tutorials

Starting off, this is for version 3.xx which is now outdated--partially the reason I wanted to begin here. I figured an older app would have less anti- techniques involved. Also, I redacted the name of the binary from the images because this is purely for educational/documentation purposes. 

With some string searches from Ida, Olly, and W32dasm, we see something promising from W32dasm.

[img removed]

So, let's search for that instruction in our Olly. Moving up out of the <code>JA</code> segment, let's see the <code>CMP</code>.

[img removed]

Follow the memory address in the hex dump below the code and set up a <strong>breakpoint on memory write</strong> to see what we're comparing with 0.

[img removed]

With the breakpoint setup, f9 and run the application. 

[img removed]

Follow that <code>CALL</code> and we'll find ourselves in one of many large functions. 

[img removed]

Take a look at the comments to the side; address <strong>OurApp.011EB5C0</strong> is another call to another large function. I've omitted that piece of the reversing because my notes are scrambled and rather messy. It's just important to note that the return of <strong>OurApp.11EB5C0</strong> is incredibly important. After we return, there's a check on AL--nop that out.

[img removed]

Save the new set of instructions as another binary and have a go. It should be noted that I've omitted everything regarding the key-file; didn't feel that typing that up would be of too much benefit either (maybe in the next writeup).

Next up: version 4.xx.
