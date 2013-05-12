Title: KeyMe2 by haggar
Date: 2011/10/26 22:30
Author: Ken Ko
Tags: crackme, keygen, reversing

<strong>The serial that works:</strong>

<code>abcd.no=54321:qw:rty12345:BFF73457</code>

Searching for any strings that may be useful.

<code>
Text strings referenced in KeyMe2:.text, item 28
Address=004015FF
Disassembly=PUSH KeyMe2.0040315C
Text string=ASCII "Registered!"
</code>

Scroll up a bit from the address and we see the beginning of the block of instructions.

<code>
004015A3 /$ A1 B0324000 MOV EAX,DWORD PTR DS:[4032B0]
</code>

That address constant, however, is referenced here:

<code>
0040153E |. A3 B0324000 MOV DWORD PTR DS:[4032B0],EAX
</code>

You can actually find the list of calls to the various anti-debug checks and such here:

<code>
00401336 |&gt; E8 24000000 CALL KeyMe2.0040135F
0040133B |. E8 74000000 CALL KeyMe2.004013B4
00401340 |. E8 D7000000 CALL KeyMe2.0040141C
00401345 |. E8 1D010000 CALL KeyMe2.00401467
0040134A |. E8 AD010000 CALL KeyMe2.004014FC
0040134F |. E8 E5010000 CALL KeyMe2.00401539
00401354 |. E8 F9010000 CALL KeyMe2.00401552
00401359 |. E8 45020000 CALL KeyMe2.004015A3
0040135E \. C3 RETN
</code>

Just break on these. How to find? Step through the program, is my method; probably not the best.

Another try...

<strong>Winning numbers: </strong>abcd.no=54321:qw:rty12345:BFF73457

<code>
64 63 62 61
D C B A
</code>

string starts at [403250]

[ebx] = dcba
[403280] = ebx

[40325C + ecx] = [403260] == 3A
--&gt; assert s[16] == ':'

[403265 + ecx] = [403269] == 3A
--&gt; assert s[25] == ':'

[403272] == 00
--&gt; assert s[34] == '\0'

[40326e + ecx] = [403272] = 00

<em>Summary:<em>
[403280..3] = "abcd"
serial[16] == serial[25] == ':'
serial[34] == '\0'</em></em>

<strong>
00401340 |. E8 D7000000 CALL KeyMe2.0040141C
</strong>

ebx = 0

ebx = [403254 + ecx] = [403258] = 0x32333435 = "5432"
[403290] = ebx

ebx = [403258 + ecx] = [40325C] = 0x77713A31 = "wq:1"
[403294] = ebx

ebx = [40325D + ecx] = [403261] = 0x31797472 = "1ytr"
[403298] = ebx

ebx = [403261 + ecx] = [403265] = 0x35343332 = "5432"
[40329C] = ebx

ebx = [403266 + ecx] = [40326A] = 0x37464642 = "BFF7"
[4032a0] = ebx

ebx = [40326A + ecx] = [40326e] = 0x37353433 = "7543"
[4032a4] = ebx

<em>Summary:</em>
[403290..a4] = "54321qwrty12345BFF73457"

<strong>
00401345 |. E8 1D010000 CALL KeyMe2.00401467
</strong>

[403250..40327C] = 0

<strong>
0040134A |. E8 AD010000 CALL KeyMe2.004014FC
</strong>

strlen([403280])
--&gt; eax = 4, edx = 'bcd'

<code>
ebx = ecx = 0
ebx = eax = 4
loop:
ecx = [40327f + ebx] = [403283] = 'd'
assert IsCharAlphaA(ecx)
ebx--
ecx = 'c'
assert IsCharAlphaA(ecx)
ebx--

</code>

<em>Summary:</em>
foreach c in [403280]:
assert IsCharAlphaA(c)
Note: [403280] is the place for the first four chars of the serial.

<strong>
0040134F |. E8 E5010000 CALL KeyMe2.00401539
</strong>

GetLogicalDrives()
[4032B0] = EAX = FC = 1111 1100 = [CDEFGH] drives are available
GetVersion() ; operating system version information
[4032B4] = 1DB10106

<em>Summary:</em>
[4032b0] = 1111 1100

00401354 |. E8 F9010000 CALL KeyMe2.00401552

<code>
eax = ebx = ecx = 0
outer:
eax = [403280 + ebx] = 'a' ; serial[0]
is eax == '\0':
jmp 0040157B
else:
inner:
xor [4032b0 + ecx], al ; xor FC, serial[ecx]
ecx++
ror [4032b0 + ecx], cl ; ror FC, ecx
if ecx != 8:
jmp 00401564
else:
jmp inner
ecx = 0
ebx++
goto outer
0040157B:
eax = ebx = ecx = 0
00401581:
eax = [403290 + ebx] = [403290] ; '5432 1qwr ty12 345B FF73 457'
xor [4032b0 + ecx], al
ecx++
ror [4032b0 + ecx], cl ; ror [eax+ecx], cl
if ecx != 8:
jmp 00401588
ecx = 0
ebx++
if ebx != 10h
jmp 00401581
retn
</code>

At this point I lost interest. Mostly, it was the anti-debug techniques that kept me with this for a while.
