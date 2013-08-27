Title: trythis0ne: OS Login
Date: 2011/10/05 00:32
Author: Ken Ko
Tags: trythis0ne.com, paros, proxy
Category: tutorials

They give you the source of their authenticating PHP file, so let's check it out. 

Looks like they're looking for a variable $admin to be set to '1'; time to install Paros Proxy. I'm not familiar with any other proxies that provide a similar functionality and it's just something I'm accustomed to from class, those many years ago. 

Once we setup a proxy on the LAN for localhost:8080 (what Paros uses by default) we simply add

<code>
&admin=1
</code>

to the POST that's going over the wire. 

Simple enough.
