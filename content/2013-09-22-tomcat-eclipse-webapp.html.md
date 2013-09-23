Title: Tomcat, Eclipse, Webapp
Author: Ken Ko
Date: 2013-09-22
Tags: coding, tomcat, eclipse, webapp
Category: blog

This is a compilation of issues needing to be dealt with.
That's the only sense of coherency for this post. For readers
other than myself, this will likely be meaningless.

Importing a Maven/Tomcat webapp into Eclipse (Kepler) EE, I've
run into a few issues. First, looks like an issue with a 
src/main/tomcat/webapp/WEB_INF/web.xml.

<pre>
<code>
&lt;web-app xmlns="http://java.sun.com/xml/ns/j2ee"
</code>
</pre>

Highlighting the line in question, we're presented with an error 
message that contains the following substring:

<pre>
<code>
contains errors (http://java.sun.com/xml/ns/j2ee/web-app_3_0.xsd)
</code>
</pre>

To remedy this, simply replace *j2ee* with *javaee* for the
following:

<pre>
<code>
&lt;web-app xmlns="http://java.sun.com/xml/ns/javaee"
</code>
</pre>

The next issue is with Tomcat being unable to run, for the
following reason in the Console:

<pre>
<code>
Caused by: java.lang.NoClassDefFoundError: Lorg/slf4j/Logger;
...
Caused by: java.lang.ClassNotFoundException: org.slf4j.Logger
</code>
</pre>

This was remedied with adding slf4j-api-$VERSION.jar and 
jul-to-slf4j-$VERSION.jar to TOMCAT_HOME/bin.

At this point, Tomcat was finally running via Eclipse. However,
the new issue occured when trying to access the servlet via URI.
Here, we got:

<pre>
<code>
java.lang.NoClassDefFoundError: org/slf4j/spi/LoggerFactoryBinder
</code>
</pre>

To address this, we needed to update the pom.xml to include:

<pre>
<code>
    &lt;dependency&gt;
        &lt;groupId&gt;org.slf4j&lt;/groupId&gt;
        &lt;artifactId&gt;slf4j-api&lt;/artifactId&gt;
        &lt;version&gt;1.7.5&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.slf4j&lt;/groupId&gt;
        &lt;artifactId&gt;jul-to-slf4j&lt;/artifactId&gt;
        &lt;version&gt;1.7.5&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;ch.qos.logback&lt;/groupId&gt;
        &lt;artifactId&gt;logback-classic&lt;/artifactId&gt;
        &lt;version&gt;1.0.13&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;ch.qos.logback&lt;/groupId&gt;
        &lt;artifactId&gt;logback-core&lt;/artifactId&gt;
        &lt;version&gt;1.0.13&lt;/version&gt;
    &lt;/dependency&gt;
</code>
</pre>

Finally, no issues.
