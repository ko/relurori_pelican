Title: shellcode: pause()
Date: 2011/09/13 23:35
Tags: nasm, shellcode, linux
Author: Ken Ko
Category: tutorials

<code class="asm">
; file: pause.asm
SECTION .text
global main
global _start</code>

main:
_start:

xor eax,eax
mov al, 29 ; pause
int 0x80
</code>

To run:

<code class="bash">
nasm -felf64 pause.asm
gcc -o pause pause.o -nostartfiles -nostdlib
./pause
</code>

Running objdump, I get:

<code class="asm">
\x31\xc0\xb0\x1d\xcd\x80
</code>

The only trouble is that when I test it with a simple main() and function pointer, Segmentation Fault. I installed <em>gdb</em> but then got carried away... now I'm doing a full update of my system. Perhaps this is a con of rolling releases? The same pro that moved me to arch!
