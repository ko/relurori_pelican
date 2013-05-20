Title: CrackME.exe by fr1c
Date: 2011/10/12 22:55
Author: Ken Ko
Tags: strings, crackme, ida pro

Found under the directory:

<code>
Crackmes.de-frozen-05-2011\crackme_1
</code>

Ran this in ida and took a gander through the strings window--doesn't hurt to check for hard coded serial numbers, ya? 

Lo and behold! Saw the following strings:

<code>
. . .
RBorland C++ - Copyright 1996 Borland Intl.
F988f91
Very good!
CrackMe by Fr1c
REGISTERED
Try again!
. . .
</code>

Guess which one is the serial.
