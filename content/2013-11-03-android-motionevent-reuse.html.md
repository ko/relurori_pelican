Title: Android MotionEvent Reuse
Author: Ken Ko
Date: 2013-11-03
Tags: coding, android, MotionEvent
Category: tutorials

Note for future reference: It's not advised to "keep copies" of
a MotionEvent. For instance the following won't be as expected.

<pre>
onTouchEvent(MotionEvent event) {
    switch(action) {
    case ACTION_DOWN:
        myDownEvent = event;
        break;
    }
}
</pre>

We'll want to do something along the lines of 

<pre>
myDownEvent.obtain(event);
...
myDownEvent.recycle();
</pre>


This is because the MotionEvent objects are appear to be preallocated 
and a part of a pool. It's clearly 
[in the documentation](http://developer.android.com/reference/android/view/MotionEvent.html) described that a MotionEvent is assigned on ACTION_DOWN
and released when ACTION_UP is encountered. 

This only caused a few days of delay.
Lol.
