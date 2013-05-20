Title: Extract and size of shellcode from objdump
Date: 2011/10/11 00:03
Author: Ken Ko
Tags: shellcode, objdump

Because I am <em>not</em> going to do this by hand for a second time.

<code>
objdump -d /tmp/ko | grep -v '<.*>:' | grep -v 'file' | grep -v '\..*:' | cut -f2 -d: | cut -f1-11 -d' ' | tr -s '\t' ' ' | sed -s 's/ $//g' | sed -s 's/ /\\x/g' | sed -e ':a;N;$!ba;s,\n,,g' | sed -e 's,^,",' | sed -e 's,$,",'
</code>

Thank you, me.

Oh, don't forget to replace that <strong>/tmp/ko</strong> with whatever you want.

Also, append the following for the length of your shellcode:

<code>
... | awk '{c += gsub(s,s)}END{print c}' s='x'
</code>
