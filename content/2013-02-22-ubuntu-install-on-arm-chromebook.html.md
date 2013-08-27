Title: Ubuntu Install on ARM Chromebook
Date: 2013/02/22 16:51
Author: Ken Ko
Tags: ubuntu, chrubuntu, chromebook
Category: tutorials

Synopsis
========
Notes for future reference. This goes through installing ChrUbuntu 
on a Samsung ARM Chromebook which houses the Exynos 5 SoC. We then
upgrade the image from Ubuntu 12.04 LTS to Ubuntu 13.04.

Method
======
Begin by powering off your machine. Before powering on, hold the following
sequence on the keyboard:

<pre>
<code>
    [esc] + [Refresh/F3]
</code>
</pre>

Press the [Power] button to enter the Recovery mode where you'll want to
follow up with the sequence of keystrokes below:

<pre>
<code>
    [ctrl] + [D]
    [Enter]
</code>
</pre>

Wait around while it downloads(verify) and wipes out the user partition.
You'll be presented with the Startup Wizard. 
Choose your wireless network, and Continue.

When prompted for your GOOG credentials, press 

<pre>
<code>
    [ctrl] + [alt] + [Forward/F2]
</code>
</pre>

Login as _chronos_. There is no password.
Once in, run the following:

<pre>
<code>
    wget http://goo.gl/34v87; sudo bash 34v87
</code>
</pre>

Apparently 10 GiB reserved for ChrUbuntu will leave ChromeOS less than
1 GiB of space. I'm going with 8 GiB, and intend to abuse the /opt mount
which I expect to be an sd card or a usb drive. 

After your disk is partitioned, choose your wireless network again.
At the GOOG credential screen, go back to the terminal:

<pre>
<code>
    [ctrl] + [alt] + [Forward/F2]
</code>
</pre>

Run the wget call once more:

<pre>
<code>
    wget http://goo.gl/34v87; sudo bash 34v87
</code>
</pre>

The script will take notice that the disk is partitioned and actually 
install the related files. You'll notice that they are prefixed with 
the string _ubuntu-1204-arm_. Wait a while because we need to download
and extract 52 files.

After the downloads are done there will be a reboot and you'll be presented
with the Unity UI. Your credentials are user/user. Open up a Terminal 
window

<pre>
<code>
    [ctrl] + [alt] + [t]
</code>
</pre>

Edit the _sources.list_ to point to 'raring' and update your apt cache(?).
If you left your computer for a few hours and Ubuntu went to sleep, don't forget
to reconnect to your wifi. Otherwise you'll have failed the apt-get update. 

<pre>
<code>
    sudo vi /etc/apt/sources.list
    :%s/precise/raring/g
    :q
    sudo apt-get update
    sudo apt-get dist-upgrade
</code>
</pre>

When doing this, my install will require 199 MiB additional disk space. Not bad
considering 1.8 GiB is used, with 5.8 GiB available. This is coming from an 8 GiB
partition from the initial bash-script-after-wget call. 

Oh, it may take a while. The mirror is from ubuntu.com... so it's not actually a mirror. 

If you come across an ncurses screen regarding _Configuring libc6_, I went with the Yes
option. This is ragarding reboots-without-prompting during the package upgrade 
process. 

The install fails with dpkg returning an error code of 1. Not sure what that's about. 
Looks like a lot of the unity packages are missing. Go with the following:

<pre>
<code>
    sudo apt-get -f install
</code>
</pre>

Follow this up with

<pre>
<code>
    sudo apt-get install ubuntu-desktop gnome-control-center nautilus nautilus-share \
                         nautilus-sendto eog unity libgnome-desktop-3.4 \
                         gnome-settings-daemon
</code>
</pre>

If you paid attention, there were errors. I'm ignoring them.
Continuing on, add the chromebook hacker's ppa. 
If you see a message about "root device does not exist", ignore it.

<pre>
<code>
    sudo add-apt-repository ppa:chromebook-arm/ppa
    sudo apt-get update
    sudo apt-get install cgpt vboot-kernel-utils linux-image-chromebook
    sudo apt-get autoremove
    sudo apt-get remove flash-kernel
</code>
</pre>

Create a temp file for the kernel boot parameters, and sign the kernel. 

<pre>
<code>
    echo "console=tty1 printk.time=1 quiet nosplash rootwait root=/dev/mmcblk0p7 rw rootfstype=ext4" > CMDLINE_FILE
    vbutil_kernel --pack /boot/chronos-kernel-image \
    --keyblock /usr/share/vboot/devkeys/kernel.keyblock --version 1 \
    --signprivate /usr/share/vboot/devkeys/kernel_data_key.vbprivk \
    --config CMDLINE_FILE --vmlinuz /boot/vmlinuz-3.4.0.5-chromebook --arch arm
</code>
</pre>

Now that you have a kernel at _/boot/chronos-kernel-image_, let's write it to disk and
set the next reboot to be in Ubuntu. If you omit the _dd_, you'll find yourself searching
around for a but related to plymouthd and a failed assertion. Apparently it is 
related to a kernel boot parameter pointing to the wrong console, but I have not 
verified the root cause. I only know this because I forgot the dd in a previous install. 

<pre>
<code>
    sudo dd if=/boot/chronos-kernel-image of=/dev/mmcblk0p6 bs=512
    sudo cgpt add -S 0 -T 1 -P 12 -i 6 /dev/mmcblk0
</code> 
</pre>

Go and reboot. 

Now you'll be seeing a blue screen instead of Unity2d. Try the key combination

<pre>
<code>
    [ctrl] + [alt] + [Previous Page/F1]
</code>
</pre>

and you should have brought up a text console. Credentials have not changed, so user/user.
Install the Mali GPU drivers for this thing: 

<pre>
<code>
    sudo apt-get install chromium-mali-opengles
</code>
</pre>

This still doesn't help Unity so let's try something else: enable the universe.

<pre>
<code>
    sudo vi /etc/apt/sources.list
</code>
</pre>

You'll want to uncomment the relevant lines and update your cache once more. This 
process may take a while because ubuntu.com is not a fast mirror for ubuntu.com

<pre>
<code>
    sudo apt-get update
</code>
</pre>

So, apparently Unity2D has been deprecated; time to look for alternatives.

Installing xmonad comes with ~600 MiB of additional stuff... dwm with ~349 KiB. 
I use them both similarly, without much customization, so let's go with dwm. However,
it does appear to be that gcc is not installed. Will need to change that. Let's just
tack on vim while we're at it, though. Small enough of a download (~24 MiB). On the other
hand, XFCE is only 181 MiB away.

<pre>
<code>
    sudo apt-get install dwm
    sudo apt-get install vim
</code>
</pre>

Now, if you want to use dwm/xmonad/xfce/whatever, edit _/etc/lightdm/lightdm.conf_. 

Go ahead and install the 'armsoc' xorg drivers, now.

<pre>
<code>
    sudo apt-get install xserver-xorg-video-armsoc
</code>
</pre>

Are you in ChromeOS? Bring up that terminal window and enter:

<pre>
<code>
    sudo cgpt add -i 6 -P 5 -S 1 /dev/mmcblk0
</code>
</pre>

If you want to have only the next reboot go into Ubuntu,

<pre>
<code>
sudo cpgt add -S 0 -T 1 -P 12 -i 6 /dev/mmcblk0
</code>
</pre>


Reboot from the main screen and you'll be loading Ubuntu. 

Alternatively...
================
Apparently there's a modified script to install [Lubuntu] with less interaction.
You can find it at this gist: 

<pre>
<code>
    https://gist.github.com/vvuk/4986933
</code>
</pre>

References
==========
http://chromeos-cr48.blogspot.co.uk/2012/10/arm-chrubuntu-1204-alpha-1-now.html
http://marcin.juszkiewicz.com.pl/2013/02/16/how-to-update-chrubuntu-12-04-to-ubuntu-13-04/
https://gist.github.com/vvuk/4986933/

