Title: Orthogonal to Isometric Tiles
Date: 2013/06/10 
Tags: game, map, isometric, tile 
Author: Ken Ko

Situation is this: I have isometric tiles being tiled as if they were
orthogonal. 

Sounds simple. Simply rotate your map by 45 degrees and ta-da you're 
isometric! If only it were that simple. The associated code is here: 

<pre>
<code>
63             // translate orthogonal to isometric
64             if (scene.data.orientation == 'isometric') {
65                 t_x = (t_i * scene.data.tilewidth / 2) - (t_j * scene.data.tilewidth / 2);
66                 t_y = (t_i * scene.data.tileheight / 2) + (t_j * scene.data.tileheight / 2);
67                 // offset the x axis since isometric is effectively a rotate 45
68                 s_x = -t_x + offset;
69                 s_y = t_y;
70             }
</code>
</pre>

Where the variables <pre><code>t_x, t_y</code></pre> are the cartesian
coordinates that will result in the isometric map. Then, we have
<pre><code>t_i, t_j</code></pre> which are the indices if the tiles were
maintained on a normal 2d array--as if they were orthogonal tiles.

The <pre><code>offset</code></pre> is the delta along the x axis to
compensate for one of the corners (max(i),0) being the most negative 
point along the x axis. Rather, because (0,0) starts at the top left
corner of the canvas, anything with a negative x value means it isn't
shown. 

That's a problem.

Fixing this required:

<pre>
<code>
44         // offset is at the (max(i),0) point. that one corner.
45         // along the x axis.
46         var offset = ((layer.height-1) * scene.data.tilewidth / 2);
</code>
</pre>

Simple, after the fact. Beforehand requires some visualization and/or paper.

Paper really helps. 
