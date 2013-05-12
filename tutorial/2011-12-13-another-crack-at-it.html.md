Title: another crack at it
Date: 2011/12/13 21:47
Author: Ken Ko
Tags: reversing, cracking, registration, serial, tutorial, writeup

Alright, let's take a look at the newest version of the application of the prior post: 4.0x as opposed to 3.9x in our first crack at it.

Start off again with the w32dasm 
<a href="http://my.yaksok.net/wp-content/uploads/2011/12/011.png"><img src="http://my.yaksok.net/wp-content/uploads/2011/12/011.png" alt="" title="01" width="589" height="102" class="alignnone size-full wp-image-183" /></a>

Looks rather familiar, no? Let's look for the same <code>push 369</code> in olly. 

<a href="http://my.yaksok.net/wp-content/uploads/2011/12/01-5.png"><img src="http://my.yaksok.net/wp-content/uploads/2011/12/01-5.png" alt="" title="01-5" width="822" height="367" class="alignnone size-full wp-image-193" /></a>

Because the window title string "... evaluation ..." was loaded around this point, we can assume the registration check occurred before this. 

[codebox 1]

If we take the jump, we skip the entire process of the "evaluation"-string concatenation to the title. Thus, I take it that the registration is even <em>before</em> that, and somehow relevant. With some more digging, we find a code block similar to 3.9x.

<a href="http://my.yaksok.net/wp-content/uploads/2011/12/02.png"><img src="http://my.yaksok.net/wp-content/uploads/2011/12/02.png" alt="" title="02" width="633" height="340" class="alignnone size-full wp-image-194" /></a> 

Looks similar, no? I started off with a patch that overwrote <code>PUSH EBP</code> with the end, <code>RETN 4</code>. That changed the visual aspects such as the window title and Help>About output. So, what about the actual functionality? Let's try to fix that.

We find two calls to that similar block:

<a href="http://my.yaksok.net/wp-content/uploads/2011/12/041.png"><img src="http://my.yaksok.net/wp-content/uploads/2011/12/041.png" alt="" title="04" width="577" height="56" class="alignnone size-full wp-image-196" /></a>

and

<a href="http://my.yaksok.net/wp-content/uploads/2011/12/051.png"><img src="http://my.yaksok.net/wp-content/uploads/2011/12/051.png" alt="" title="05" width="643" height="46" class="alignnone size-full wp-image-197" /></a>

Since we can't change that <code>MOV BYTE PTR DS:[12B70A0],AL</code> to <code>MOV BYTE PTR DS:[12B70A0],4 </code> because they aren't the same size, let's call this at the end of "similar codeblock" and NOP out the CALL we see above:

<a href="http://my.yaksok.net/wp-content/uploads/2011/12/07.png"><img src="http://my.yaksok.net/wp-content/uploads/2011/12/07.png" alt="" title="07" width="570" height="95" class="alignnone size-full wp-image-199" /></a>

and

<a href="http://my.yaksok.net/wp-content/uploads/2011/12/08.png"><img src="http://my.yaksok.net/wp-content/uploads/2011/12/08.png" alt="" title="08" width="576" height="86" class="alignnone size-full wp-image-200" /></a>

Now, let's change the end of the "similar codeblock" to store the return value. We changed this:

<a href="http://my.yaksok.net/wp-content/uploads/2011/12/03.png"><img src="http://my.yaksok.net/wp-content/uploads/2011/12/03.png" alt="" title="03" width="570" height="169" class="alignnone size-full wp-image-195" /></a>

to this:

<a href="http://my.yaksok.net/wp-content/uploads/2011/12/061.png"><img src="http://my.yaksok.net/wp-content/uploads/2011/12/061.png" alt="" title="06" width="568" height="75" class="alignnone size-full wp-image-198" /></a>

With this patch, the app is cracked; fun effort. I'll close with a list of breakpoints I had setup by the end of the journey:

<a href="http://my.yaksok.net/wp-content/uploads/2011/12/breakpoints.png"><img src="http://my.yaksok.net/wp-content/uploads/2011/12/breakpoints.png" alt="" title="breakpoints" width="834" height="230" class="alignnone size-full wp-image-201" /></a>
