Title: Rev by Basse
Date: 2011/10/29 16:53
Author: Ken Ko
Tags: crackme, keyboard, hook
Category: tutorials

Exploration Phase
=================
Run through this binary and make what we can of it on our first pass.

<code>
00401057   . C705 FF304000 >MOV DWORD PTR DS:[4030FF],BAD0DEAD
00401061   . C605 08314000 >MOV BYTE PTR DS:[403108],35
</code>

DS:[4030FF] = BAD0DEAD\x35

<code>
00401068   . 6A 00          PUSH 0                                   ; /Text = NULL
0040106A   . 68 B80B0000    PUSH 0BB8                                ; |ControlID = BB8 (3000.)
0040106F   . FF75 08        PUSH DWORD PTR SS:[EBP+8]                ; |hWnd
00401072   . E8 27020000    CALL <JMP.&USER32.SetDlgItemTextA>       ; \SetDlgItemTextA
</code>

So, SetDlgItemTextA does the following: <em>Retrieves a handle to a control in the specified dialog box</em>. Probably helpful for the only dialog box visible to us.

<code>
00401077   . 58             POP EAX
00401078   . 3D F700FB02    CMP EAX,2FB00F7
0040107D   . 75 29          JNZ SHORT Rev.004010A8
</code>

At the pop, we have:

<code>
[0012faa0] = BAD0DEAD
EAX = 1h
</code>

At the compare, though, <code>EAX=BAD0DEAD</code> when we really want <code>2FB00F7</code>. 

Alas, "Not even close". 

Second Pass
===========
Let's look around for some interesting fucntions--yeah, should have really done that first. I know.

<code>
00401153   . 6A 00          PUSH 0                                   ; /ThreadID = 0
00401155   . FF35 09314000  PUSH DWORD PTR DS:[403109]               ; |hModule = 00400000 (Rev)
0040115B   . 68 C0114000    PUSH Rev.004011C0                        ; |Hookproc = Rev.004011C0
00401160   . 6A 03          PUSH 3                                   ; |HookType = WH_GETMESSAGE
00401162   . E8 49010000    CALL <JMP.&USER32.SetWindowsHookExA>     ; \SetWindowsHookExA
</code>

From microsoft.com: <em>Installs an application-defined hook procedure into a hook chain. You would install a hook procedure to monitor the system for certain types of events. These events are associated either with a specific thread or with all threads in the same desktop as the calling thread.</em>

Then, let's look at what microsoft.com shows us for WH_GETMESSAGE: <em>Installs a hook procedure that monitors messages posted to a message queue. For more information, see the GetMsgProc hook procedure.</em>

The process in question is located at Rev.004011C0 so let's take a gander, there.

<code>
004011C0   . 55             PUSH EBP
004011C1   . 8BEC           MOV EBP,ESP
004011C3   . 837D 08 00     CMP DWORD PTR SS:[EBP+8],0               ;  strcmp?
004011C7   . 73 1A          JNB SHORT Rev.004011E3
004011C9   . FF75 10        PUSH DWORD PTR SS:[EBP+10]               ; /lParam
004011CC   . FF75 0C        PUSH DWORD PTR SS:[EBP+C]                ; |wParam
004011CF   . FF75 08        PUSH DWORD PTR SS:[EBP+8]                ; |HookCode
004011D2   . FF35 03314000  PUSH DWORD PTR DS:[403103]               ; |hHook = NULL
004011D8   . E8 9D000000    CALL <JMP.&USER32.CallNextHookEx>        ; \CallNextHookEx
004011DD   . C9             LEAVE
004011DE   . C2 0C00        RETN 0C
004011E1   . EB 73          JMP SHORT Rev.00401256
004011E3   > 837D 08 00     CMP DWORD PTR SS:[EBP+8],0               ;  JNB destination. hash?
</code>

We do a null check on the first byte to check for empty strings. If there is nothing, continue on with calling the next hook. Else, jump to 0x004011E3 and calculate a hash. 

The instructions following 0x004011E3 look like they're for recalculating the hash. So, it looks like they recalc the hash every time a key is entered via this hook, with the hash initiated as 0xBAD0DEADh. 

Anyhow, let's patch the binary after having a general idea of how this binary hides its serial calculation. 

<code>
00401077   . 58             POP EAX
00401078   . 3D F700FB02    CMP EAX,2FB00F7
0040107D     75 29          JNZ SHORT Rev.004010A8
0040107F   . 6A 40          PUSH 40                                  ; /Style = MB_OK|MB_ICONASTERISK|MB_APPLMODAL
00401081   . 68 AA304000    PUSH Rev.004030AA                        ; |Title = "Rev"
00401086   . 68 79304000    PUSH Rev.00403079                        ; |Text = "Good job! You made it!
Send the solution to ..."
0040108B   . FF75 08        PUSH DWORD PTR SS:[EBP+8]                ; |hOwner
0040108E   . E8 FF010000    CALL <JMP.&USER32.MessageBoxA>           ; \MessageBoxA
00401093   . 68 70304000    PUSH Rev.00403070                        ; /Text = "Success!"
00401098   . FF35 0D314000  PUSH DWORD PTR DS:[40310D]               ; |hWnd = NULL
0040109E   . E8 07020000    CALL <JMP.&USER32.SetWindowTextA>        ; \SetWindowTextA
</code>

Change 0x0040107D from a <code>JNZ</code> to a <code>JE</code>.

Yup. Keyboard hooks are pretty cool.
