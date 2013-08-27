Title: Android OpenGL onSurfaceCreated
Date: 2013/05/31 
Tags: android, opengl
Author: Ken Ko
Category: tutorials

My commit message:

<pre>
<code>
Fix build issue in BoardRenderer regarding Override.

Imported android.opengl.EGLConfig but the GLSurfaceView.Renderer was 
expecting the EGLConfig hanging off the javax.microediting.khronos.egl 
package.
</code>
</pre>

Problem appears to be that when I (wrongfully) imported <pre><code>android.opengl.EGLConfig</code></pre> instead of <pre><code>javax.microediting.khronos.egl.EGLConfig</code></pre> it was all for naught. 

I suspected that my use of Android Studio instead of Eclipse/ADT was
the cause of some build issue and ended up finding mentions of java 
applications (to be differentiated from Android applications) using gradle
and setting an explicit <pre><code>sourceCompatibility = 1.6</code></pre>. By the way,
that doesn't do anything in Android Studio. Having a java plugin
alongside an android plugin (in terms of Gradle) is a no-no.

For future reference.
