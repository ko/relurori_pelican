Title: Crackme 7 by Detten
Date: 2011/10/18 00:02
Author: Ken Ko
Tags: python, crackme, keygen

<code>
00401124   > 68 97314000    PUSH ko1.00403197                        ; /ProcNameOrOrdinal = "GetDlgItemTextA"
00401129   . FF35 30324000  PUSH DWORD PTR DS:[403230]               ; |hModule = NULL
0040112F   . E8 88010000    CALL <JMP.&kernel32.GetProcAddress>      ; \GetProcAddress
00401134   . 8038 CC        CMP BYTE PTR DS:[EAX],0CC
00401137   . 75 05          JNZ SHORT ko1.0040113E
00401139   .^E9 F9FEFFFF    JMP ko1.00401037
</code>

INT3 = CCh for when we place a breakpoint. Then, GetProcAddress will return CCh instead of the address of GetDlgItemTextA--in this scenario. We see something similar for other API calls as well. Eventually we'll see the "Stop using a debugger!" message. 

Also worth noting is that address <strong>0x00401037</strong> isn't the start of an instruction. What's that about? The instruction 0x00401035 is <strong>PUSH 68006A05</strong> so what if we NOP the addresses <strong>0x00401035</strong> and <strong>0x00401036</strong>? We now have <strong>0x00401037</strong> to be <strong>PUSH 0</strong>. Should be easier to read, now.

Algorithm so far:

<code>
ESI = 0xDEE1h
for (i = 0; i < strlen(EAX); i++) {
	ESI += EAX[i]
	ESI %= EAX[i]
}
"""
Reverse this
EAX += SHL(EAX,4)
EAX += 0x0DEAD
EAX += ROL(EAX,2)
CMP ESI, EAX
"""
s += ROR(s,2)
s -= 0x0DEAD
s += SHR(s,4)

print s
</code>

The actual:

[codebox 1]

I couldn't get a key for 'kenko' but got one for 'detten'. When all else fails, try to keygen the author's handle!
