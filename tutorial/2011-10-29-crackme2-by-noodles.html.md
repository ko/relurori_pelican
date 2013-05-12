Title: crackme2 by noodles
Date: 2011/10/29 22:48
Author: Ken Ko
Tags: crackme

We're looking for a <strong>spook.key</strong>, so make that file. 

This looks like the algorithm being used by the app:

<code>
00401511   . B8 FF354000    MOV EAX,noodles-.004035FF
00401516   . C100 05        ROL DWORD PTR DS:[EAX],5
00401519   . 8300 0F        ADD DWORD PTR DS:[EAX],0F
0040151C   . C148 04 07     ROR DWORD PTR DS:[EAX+4],7
00401520   . 8368 04 05     SUB DWORD PTR DS:[EAX+4],5
00401524   . 8178 04 BDD842>CMP DWORD PTR DS:[EAX+4],C642D8BD
0040152D   . 8138 FC098E2E  CMP DWORD PTR DS:[EAX],2E8E09FC
</code>

<em><strong>or</strong></em>

... patch the binary with the following changes:

<code>
004014E6	JNZ -> JE
0040152B	JNZ -> JE
00401533	JNZ -> JE
</code>

Yup. I went with the patching.
