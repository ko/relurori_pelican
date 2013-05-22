Title: Pathfinding Brainstorm
Date: 2013/05/22 00:42
Tags: game, development, ai, pathfinding, thoughts
Author: Ken Ko

**Disclaimer:** This is all without having actually looked at more
advanced pathfinding algorithms. Or any algorithms, really. More to
be a container for thoughts.

Some background. This topic came up while working on a simple 2d 
game engine. Laying out the skeleton and working on the board
implementation and technical design, it occured to me that it would
be _cool_ to have pathfinding. Necessary? Not really. But cool, yes.

So I went ahead and thought up the most naive algorithm I could and
went and implemented that. 

Onward to the algorithm!

Imagine two representations for the same map. 

1. Cartesian coordinates
2. Isometric tiles

Using the Cartesian coordinates, we find a direct line between the
start (A) and end (B) positions. Travel along that line and find the
tile that maps to (and thereby contains) this coordinate. Add the
tile to a list. 

Repeat the above for all points along the line and you should have
a list of tiles that need be traversed to get from point A to 
point B. 

Difficulties arise when there are objects in the way (you don't say!). 
This part is still a work in progress (as if that first part is gold)
but the general idea is to branch off left and right when we encounter
an occupied tile. From these two points (left and right branches taken),
find a direct line to B and redo the entire process. Repeat recursively
(and implement iteratively if stack is an issue[0] for you) until you 
reach B. 

One glaring inefficiency that I see with this is that it's similar to
branch prediction done by a CPU but the wrong path can't be discarded
until _way_ later when we finally hit the destination. There simply
must be a better solution to this. 

So that's what I have so far. Considering that there are more pressing
issues to follow (like making this game engine), I may have to put my
pathfinding algorithm discovery process on hold.

[0] Imagine pathfinding in a kernel module. 8KiB stack size would 
be a fun limitation to work with for this type of problem. 
