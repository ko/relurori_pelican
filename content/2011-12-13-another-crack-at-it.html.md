Title: another crack at it
Date: 2011/12/13 21:47
Author: Ken Ko
Tags: reversing, cracking, registration, serial, tutorial, writeup
Category: tutorials

Alright, let's take a look at the newest version of the application of the prior post: 4.0x as opposed to 3.9x in our first crack at it.

Start off again with the w32dasm 

[img removed]

Looks rather familiar, no? Let's look for the same <code>push 369</code> in olly. 

[img removed]

Because the window title string "... evaluation ..." was loaded around this point, we can assume the registration check occurred before this. 

[codebox 1]

If we take the jump, we skip the entire process of the "evaluation"-string concatenation to the title. Thus, I take it that the registration is even <em>before</em> that, and somehow relevant. With some more digging, we find a code block similar to 3.9x.

[img removed] 

Looks similar, no? I started off with a patch that overwrote <code>PUSH EBP</code> with the end, <code>RETN 4</code>. That changed the visual aspects such as the window title and Help>About output. So, what about the actual functionality? Let's try to fix that.

We find two calls to that similar block:

[img removed]

and

[img removed]

Since we can't change that <code>MOV BYTE PTR DS:[12B70A0],AL</code> to <code>MOV BYTE PTR DS:[12B70A0],4 </code> because they aren't the same size, let's call this at the end of "similar codeblock" and NOP out the CALL we see above:

[img removed]

and

[img removed]

Now, let's change the end of the "similar codeblock" to store the return value. We changed this:

[img removed]

to this:

[img removed]

With this patch, the app is cracked; fun effort. I'll close with a list of breakpoints I had setup by the end of the journey:

[img removed]
