Title: Rooting an HTC Aria with ATT, 2.2.2
Date: 2011/09/15 02:05
Tags: rooting, htc, aria, cyanogenmod, att
Author: Ken Ko
Category: tutorials

<strong>Disclaimer</strong>: This was an absurd journey.

It started with this: <a href="http://forum.xda-developers.com/showpost.php?p=7449486&postcount=1">creating an ISO to run unrevoked's root exploit against the Aria</a>. The first issue is that I had no idea how to boot from CD on a mac. It's <em>c</em> while booting. Anyhow, the Ubuntu image didn't have the wireless drivers required for whatever chipset the powerbook uses. Then I tried out the Thinkpad. Found out that it doesn't boot from cd--NO idea why--so I was glad to recall that I have a USB optical drive. Thank the gods. Everything loaded up fine, but the actual unrevoked script failed. Gave me the error that it failed to root, that perhaps my firmware is too new. 

This was the beginning. Google some and we find out the the Android 2.2.2 update that AT&T pushed out OTA actually updated the HBOOT--this seems to prevent unrevoked's exploit from doing its magic. That's when I found out about Revolutionary, or alpharev. The xda forums mentioned that alpharev has a method for rooting the 2.2.2 image and I gave that a try. It <em>appeared</em> to work after all the driver installation hassle (I'm back on Windows, btw) but then it also asked if I wanted to install Clockwork. "Sure, why not", right? 

First things first, I go into HBOOT and see S-OFF. Great! Then I see messages about how we're missing LIBEDIAG and such from the SD card. I'm pretty sure, now, that that was a red herring because I never exactly resolved that. Seems that others have found this HBOOT issue as well but no actual resolution. Did learn that plugging into the usb of a computer while going into HBOOT has a bug, however. 

Then I went to look at the Clockworkmod that was installed--very customized in comparison to the previous version I had. It was 4.1.0.4 by Revolutionary. It would also flash, in large letters, "REVOLUTIONARY" when I tried to do anything past the first menu layer--including reboot! <em>Something just had to be wrong</em>.

Found <a href="http://forum.xda-developers.com/showpost.php?p=14693680&postcount=1">clockworkmod 4.1.0.4 for the HTC Liberty/Aria</a>, and I tried to flash that over. The commands boiled down to:

<code class="bash">
fastboot flash recovery recovery_name.img 
</code>

Thing is, that didn't work out too well either. Nothing changed--the Revolutionary CWM was still in place.

So, what now? Desperation. Found some guides on downgrading the 2.2.2 to 2.1 Android via a Goldcard. The xda forum's Aria Superthread had a link to the 2.1 AT&T RUU--never got to use it, though. That was interesting, though--learning about goldcards, that is, along with whatever else is involved in mobile forensics. May have to take a look into that route later on--for both Android and iOS and Windows Mobile. Could be very interesting, indeed.

I couldn't get past the idea that Revolutionary CWM 4.1.0.4 was almost working--almost. Sure, CWM is now up to version 5, but my previous Aria was still on CWM 2. Something had to be up. Lo and behold, <a href="http://forum.xda-developers.com/showpost.php?p=14861791&postcount=84">there was yet another method</a>. This one was more involved for installing CWM.

This method worked.
5.5 hours of work.

<strong>Summary: </strong>Next time I would run the alpharev and not have it install CWM. Then manually install the old, 2.5, CWM with the following commands:

<code class="bash">
adb reboot bootloader
fastboot erase cache
fastboot oem rebootRUU
fastboot flash zip clockwork2501.zip
fastboot reboot
</code>

Just make sure you wipe cache + data in clockwork before installing cyanogenmod or whatever it is you choose to use because the Android directory structure changed between 2.2 and 2.3. You'll be in a bootloop with the cyanogenmod boot screen over and over and over and over and over. Been there, done that. 
