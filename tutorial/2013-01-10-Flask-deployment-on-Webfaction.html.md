Title: Flask deployment on Webfaction
Date: 2013/01/10 21:58
Author: Ken Ko
Tags: web, flask

Note: Don't forget to modify the httpd.conf file.

<code>
    /home/$USERNAME/webapps/$APP/apache/conf/httpd.conf
    ----------------------------------------------------
    WSGIPythonPath /home/$USERNAME/webapps/$APP/htdocs/
    WSGIScriptAlias / /home/$USERNAME/webapps/$APP/htdocs/index.py

    <Directory /home/$USERNAME/webapps/$APP/htdocs>
        AddHandler wsgi-script .py
        RewriteEngine On
        RewriteBase /
        WSGIScriptReloading On
    </Directory>
</code>
