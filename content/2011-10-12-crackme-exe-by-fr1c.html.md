Title: CrackME.exe by fr1c
Date: 2011/10/12 22:55
Author: Ken Ko
Tags: strings, crackme, ida pro
Category: tutorials

Found under the directory:

<pre>
<code>
Crackmes.de-frozen-05-2011\crackme_1
</code>
</pre>

Ran this in ida and took a gander through the strings window--doesn't hurt to check for hard coded serial numbers, ya? 

Lo and behold! Saw the following strings:

<pre>
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
</pre>

Guess which one is the serial.
