Title: aolsbm.1.exe :: static analysis
Date: 2011/12/30 23:34
Author: Ken Ko
Tags: writeup, malware, analysis, static, dynamic, cuckoo

Finding the binary:
<code>
MD5:5a2be07ad750bed86be65954fb9d7d21	
SHA1:388f87542588e9298f045d6a594af9245d59abd5
</code>

<strong>Initial Static Analysis</strong>

Open the binary in Ida and we see hints that the binary is packed with UPX. Decode it and run the new binary in Olly/Ida:

[codebox 1]

Now, let's take a look at the import table and see if there's anything interesting (luckily, there actually is an import table to look at).

<a href="http://my.yaksok.net/wp-content/uploads/2011/12/013.png"><img src="http://my.yaksok.net/wp-content/uploads/2011/12/013.png" alt="" title="01" width="440" height="173" class="alignnone size-full wp-image-212" /></a>

It's generally good to know where the malware is looking to talk to, but verifying it is always nice. Looking through the string extraction:

<a href="http://my.yaksok.net/wp-content/uploads/2011/12/022.png"><img src="http://my.yaksok.net/wp-content/uploads/2011/12/022.png" alt="" title="02" width="408" height="348" class="alignnone size-full wp-image-213" /></a>

If you enter the first URL into google, we find <a href="http://malc0de.com/database/index.php?search=97.74.144.106&IP=on">a list of binaries</a> that are talking to the same server. 

<a href="http://my.yaksok.net/wp-content/uploads/2011/12/032.png"><img src="http://my.yaksok.net/wp-content/uploads/2011/12/032.png" alt="" title="03" width="394" height="117" class="alignnone size-full wp-image-214" /></a>

We find other interesting pieces of information from the strings, but we should also figure out what is being done by this malware now.

This concludes part 1; we'll see if this particular binary keeps my interest.
