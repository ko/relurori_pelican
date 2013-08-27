Title: intruded.net, behemoth: level 6
Date: 2011/10/02 01:14
Author: Ken Ko
Tags: intruded.net, behemoth, netcat
Category: tutorials

I'm so dumb.

Ran through the disassembled instructions with objdump and gdb for a long time until I decided to download IDA Freeware 5.0. In there, I saw that it's calling gethostbyname on localhost and atoi on 1337. 

Then it came to me: <em>strings</em>.

[codebox 1]

It <em>never</em> came to mind that I should run strings or look at the .rodata section of the binary. Never. That's terrible. 

[codebox 2]

Run that in a separate window. Try <strong>/wargame/level6</strong> once more. The window with netcat will show you the password. 
