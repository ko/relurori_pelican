Title: Breakout Island Collision Detection
Author: Ken Ko
Date: 2013-10-06
Tags: coding, android, game, breakout island
Category: tutorials

Basic collision detection for [breakout island](https://github.com/ko/breakout-island).
Sample code for the second revision of collision detection
(described below) can be found [here](https://github.com/ko/breakout-island/commit/5515d5e8b27caa413a8be43e91a23b94503bf6ef).

The first iteration was pretty simple; assume the following:

<pre>
<code>
Ball coordinates: (xc,yc)
Ball radius: r

Rectangle's corners:

(x2,y2)------(x1,y1)
   |            |
   |            |
(x4,y4)------(x3,y3)]
</code>
</pre>

The basics were 

<pre>
<code>
if (xc <= x1 && xc >= x2) {
    // y increases downward, not up 
    if (yc <= y4 && yc >= y2) {
        collide();
    }
}
</code>
</pre>

There are (at least) two cases that this doesn't account for:

1. Ball hitting the rectangle from the corner
2. Ball is larger than a single pixel

To address the 2nd issue, we'll do something along the lines of this:

<pre>
<code>
if (x2 <= xc && xc <= x1) {
    if (Math.abs(y2 - yc) <= r) {
        collide();
    }
}
</code>
</pre>

except for all four sides of the rectangle.

There are (at least) two cases that this doesn't account for:

1. Ball hitting the rectangle from the corner
3. Rectangle side (length or width) is > 2r
