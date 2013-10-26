Title: Breakout Island GC
Author: Ken Ko
Date: 2013-10-19
Tags: coding, android, game, breakout island
Category: tutorials

Moving my testing from a Galaxy Nexus with 4.3 to an LG G2 with 4.2.2, I've
noticed that there are many GC_FOR_ALLOC messages in Logcat. Few things 
to remedy this. Primarily, reuse objects as can be seen [in this commit](https://github.com/ko/breakout-island/commit/12a781f4f7e7638b2d4e93e0ecad5f9885fca0b0).

The first iteration of this, however, was to revert all use of iterators to
simply refering by index. An example of this can be found [here](https://github.com/ko/breakout-island/commit/516013c9669ad08511bd2a8b35d0f6bea3c7b7a1).
While it's cute to use an enhanced for loop such as

<pre><code>
for (Iterator<Object> it = object.iterator(); it.hasNext(); ) {
    Object o = it.next();
    ...
}
</code></pre>

or 

<pre><code>
for (Object object : objects) {
    ...
}
</code></pre>

the creation of an iterator becomes prohibitively expensive. Like I was
told, 

> If we see one million packets per second, this
> line of code will be executed one million times
> per second.
> ~ W.S.

This can be generalized into a warning about being careful about what
code you keep in the [fast path](http://en.wikipedia.org/wiki/Fast_path). 
In our case, we'd like to limit memory allocations to mitigate any
performance and frame drops from garbage collection running.

This is still a work in progress, but I do notice the G2 being a lot
more aggressive with the GC than the Galaxy Nexus with 4.3 appears to be.
