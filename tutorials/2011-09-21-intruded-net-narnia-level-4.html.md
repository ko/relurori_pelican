Title: intruded.net, narnia: level 4
Date: 2011/09/21 19:41
Tags: intruded.net, narnia, gdb
Author: Ken Ko

<em>Initial thought</em>: I want to overflow argv[1] into ofile to overwrite the "/dev/null" string with something in /tmp. Also, the ifile should be a symlink to /home/level5/.passwd but they check to see if ifile has O_RDWR permissions. This could be trouble.

So, what would be blocking us from a naive approach? At the moment, it's the check for whether <strong>ofile</strong> is O_RDWR permissible. To account for this:

<code>
touch /tmp/kenko
</code>

Now, we need <strong>ifile</strong> to be O_RDONLY permissible. No problem. 

<code>
mkdir /tmp/aaaaaaaaaaaaaaaaaaaaaaaaaaa/tmp
ln -s /home/level5/.passwd /tmp/aaaaaaaaaaaaaaaaaaaaaaaaaaa/tmp/kenko
chmod 777 /tmp/kenko
</code>

<em>Note</em>: We need the chmod at the end to mitigate an 'no permissions' error, thrown by the binary.

We chose to have <em>/tmp/aaaaaaaaaaaaaaaaaaaaaaaaaaa</em> as our <strong>ifile</strong> value through guess and check. We tried one less <em>a</em> but then the binary complained about <em>tmp/kenko</em> instead of <em>/tmp/kenko</em>. I suppose reading the disassembly would have been helpful in having a clearer picture of the stack. 

Now all we need to do is

<code>
cat /tmp/kenko
su level5
</code>

That was relatively easy, compared to the last two. Granted, this was just a tricky buffer overflow and the level 2 was my first time writing shellcode in 2011. Taking a long hiatus... probably not the best of ideas.
