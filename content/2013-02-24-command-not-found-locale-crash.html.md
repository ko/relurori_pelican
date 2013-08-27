Title: Command Not Found Locale Crash
Date: 2013/02/24 12:02
Author: Ken Ko
Tags: ubuntu, chrubuntu, chromebook, locale
Category: tutorials

The laziness hit; went with the Lubuntu script install method from the
gist found in a previous post. After setting up xubuntu-desktop as a
possible session (because LXDE looks like KDE2 which looks like a terrible
copy of Windows 95), typing in random trash has crashed _command-not-found_.

Something along the lines of:

<pre>
<code>
    ko@armbook:/etc/udev/rules.d$ update-local
    Sorry, command-not-found has crashed! Please file a bug report at:
    https://bugs.launchpad.net/command-not-found/+filebug
    Please include the following information with the report:

    command-not-found version: 0.3
    Python version: 3.3.0 final 0
    Distributor ID: Ubuntu
    Description:    Ubuntu Raring Ringtail (development branch)
    Release:    13.04
    Codename:   raring
    Exception information:

    unsupported locale setting
    Traceback (most recent call last):
      File "/usr/lib/python3/dist-packages/CommandNotFound/util.py", line 24, in crash_guard
        callback()
      File "/usr/lib/command-not-found", line 69, in main
        enable_i18n()
      File "/usr/lib/command-not-found", line 40, in enable_i18n
        locale.setlocale(locale.LC_ALL, '')
      File "/usr/lib/python3.3/locale.py", line 541, in setlocale
        return _setlocale(category, locale)
    locale.Error: unsupported locale setting
</code>
</pre>

The final resolution was found after seeing a _lot_ of bug reports... 

<pre>
<code>
    export LANGUAGE=en_US.UTF-8
    export LANG=en_US.UTF-8
    export LC_ALL=en_US.UTF-8
    locale-gen en_US.UTF-8
    dpkg-reconfigure locales
</code>
</pre>

References
==========
http://www.thomas-krenn.com/de/wiki/Perl_warning_Setting_locale_failed_unter_Debian
