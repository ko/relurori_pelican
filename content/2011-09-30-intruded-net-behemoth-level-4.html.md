Title: intruded.net, behemoth: level 4
Date: 2011/09/30 00:13
Author: Ken Ko
tags: intruded.net, gdb, format string, behemoth
Category: tutorials

Tried to overflow the buffer, but I couldn't do it with even 1000+ characters. Let's try something systematic this time, instead of trying to get lucky.

[codebox 1]

Looks like there's a huge buffer being created so let's try something else instead. They repeat whatever I type, maybe it's a format string?

[codebox 2]

Awesome! Found where the AAAA is. Let's go a step further and try to overwrite <strong>$eax</strong> to an arbitrary address. Unlike level 3's initial failures, I'm <em>certain</em> this will be worth figuring out for the future.

[codebox 3]

Now, where do we want to point <strong>$eax</strong> to? If we recall, <a href="http://www.epanastasi.com/?page_id=60">this page</a> delves into format string exploits and using constructor/destructor areas from GCC.

[codebox 4]

Of interest is <strong>08049598 d __DTOR_END__</strong> and <strong>08049594 d __DTOR_LIST__</strong>.

[codebox 5]

The <strong>objdump</strong> shows the section headers: note that <strong>.dtors</strong> and <strong>.ctors</strong> are not in the read-only data section.

On the hunt for additional resources, we find <a href="http://www.cgsecurity.org/Articles/SecProg/Art4/index.html">this</a> writeup by cgsecurity. It's rather detailed about how and why format strings are exploitable, if left to the user.

Take a look at gdb, once more:

[codebox 6]

Verifying our buffer address... because we can?

<code>

Address of our buffer

=====================

(gdb) r &lt;
Starting program: /wargame/level4 &lt;
(gdb) b *0x0804846a

Breakpoint 2 at 0x804846a

. . .

(gdb) x/456x $esp-456

. . .

0xbffff924: 0xb7ec3b6e 0x00000000 0x00000000 0x41414141

0xbffff934: 0x41414141 0x41414141 0x41414141 0x41414141

0xbffff944: 0x41414141 0x41414141 0x41414141 0x41414141

0xbffff930 begins our buffer.

Address of .dtor

================

level4@behemoth:/tmp$ objdump -x /wargame/level4 | grep dtor

16 .dtors 00000008 08049594 08049594 00000594 2**2

08049594 l d .dtors 00000000 .dtors

08049594 l O .dtors 00000000 __DTOR_LIST__

08048390 l F .text 00000000 __do_global_dtors_aux

08049598 l O .dtors 00000000 __DTOR_END__

level4@behemoth:/tmp$

0x08049598 ends our DTOR.
</code>

<strong>New plan of action:</strong> redirect the dtor/deconstructor to our buffer where we should then execute the shellcode.

Sound good?

[codeblock 8] (missing from session timeout)

Summary of what we know:

<code>
Offset: 8
DTORS 0x08049594  to 0x08049598
Buffer begins at 0xbffff930
</code>

Seemingly an important discovery: <string>using this method (direct parameter accessing), we can only write up to 2 bytes of memory at a time</strong>.

[codeblock 9] (missing from session timeout)

The last one is absurdly long to execute, and the address isn't even close to where we actually want. Guess we'll go for two bytes at a time?

Math time! Oh, our buffer address changed during the reboot that occurs every 6 hours. Went <strong>from</strong> 0xbffff930 <strong>to</strong> 0xbffff980. We want to skip the first <strong>8</strong> bytes of the buffer because they contain the addresses of the dtor. 

<code>
Offset to our format string: 8d
We want to write: 0xbffff988
0xbfffh = 49151d
0xf988h = 63880d

[&dtor+2][&dtor][nop *30][shellcode *61][%x *(49151 - (61+8+30))%<strong>8</strong>$n][%x *(63880 - 49151)%<strong>9</strong>$n]
</code>

Added the nops just for the hell of it. According to gdb, we should have been going straight into the shellcode with the dtor. 

Here it is, finally working:

[codebox 10]

First: what is this <strong>%hn</strong> business all about? 
Appending <strong>h</strong> to any string format parameter makes me a short version, so in this case we're writing 2 bytes instead of the normal 4 full bytes. This lets us write a memory address in 2 writes instead of 4, or 1. Didn't go with a single write because the address was definitely overflowing somewhere between 2.2 billion and 3.2 billion. I suppose it had to do with 2's complement and all, but I really didn't feel like verifying that at the time.

<strong>Address calculations</strong>
We have 2 parts we want to write: the top 2 bytes and the bottom 2 bytes. The buffer starts at 0xbffff980 but we have 8 bytes in the beginning just for the [&dtor+2] and [&dtor]. Thus, we want to jump into 0xbffff988.

The top half [&dtor+2]: 0xbfff
The bottom half [&dtor]: 0xf988

In our setup, we're writing [&dtor+2] first. So, 0xbfffh = 49151d. Subtract whatever we're written to the buffer so far: [8] the addresses, [30] the nops, [61] the shellcode. That leaves us with 49151d - 99d = 49052d as the offset of the %n for [&dtor+2].

For subsequent addresses offsets, we basically want to do <em>the address we want</em> minus <em>the address that was just written</em>. 

In our case, we want 0xf988h or 63880d. We just wrote a total of 0xbfffh or 49151d. So, the next %n offset is retrieved with 63880d - 49151d = 14729d.

If we wanted another address to write after that such as 0xbeef (48879d), 48879d - 14729d= 0x8566h (34150d). And so on and so on.

<strong>Additional references</strong>:
<a href="http://www.securiteam.com/securityreviews/6E0030KNFO.html">securiteam</a>
<a href="http://julianor.tripod.com/bc/NN-formats.txt">nop ninjas</a>
<a href="http://surface.syr.edu/cgi/viewcontent.cgi?article=1095&context=eecs">syracuse edu</a>
<a href="http://www.infosecwriters.com/texts.php?op=display&id=19">infosecwriters</a> - this is actually using malloc chunks, pretty interesting
