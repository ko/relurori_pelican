Title: 'trythis0ne: 1337browser'
Date: 2011/10/05 00:15
Author: Ken Ko
Tags: trythis0ne.com, user agent, browser
Category: tutorials

I've been yearning for another wargame with intruded.net being down; found trythis0ne.com. 

This was a pretty simple task.

View the source and see that there's a reference to http://trythis0ne.com/levels/web-challanges/1337B/pwd.php.

In firefox, go to about:config and add this new value:

<code>
general.useragent.override;1337Browser_V3.1
</code>

Visit pwd.php again, and you'll get the password.
