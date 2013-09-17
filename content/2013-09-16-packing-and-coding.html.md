Title: Packing and Coding
Author: Ken Ko
Date: 2013-09-16
Tags: thoughts, backpacking, coding
Category: blog

I've been doing some day trips, lately, to some of the more remote 
regions around the San Francisco Bay Area. While packing for a 
[a trip to Mt. Saint Helena](http://kenkophoto.com/mount-st-helenas-north-peak.html) 
I've realized that the majority of my contents are safety related:
headlamp, minor first aid equipment, knife, paracord, etc. 

When I think about the contents of my code, a lot of what I write is
error handling. For instance:

<pre>
<code>
    rc = foo(bar);
    if (rc != 0) 
        goto exit_foo;
</code>
</pre>

or in a non-ideal case:

<pre>
<code>
    rc = foo(bar);
    if (rc != 0) {
        cleanup1();
        cleanup2();
        rc2 = cleanup3();
        if (rc3 != 0) {
            ...
        }
    }
</ocde>
</pre>

That's a lot of space for a single function call. I figure packing a
bag can draw a lot of similarities to code structure in my C programs.
