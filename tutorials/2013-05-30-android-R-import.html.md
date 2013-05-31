Title: Android R Import
Date: 2013/05/30 
Tags: android
Author: Ken Ko

Encountered a fun problem, here. I was adding integers to a new file under
res/values/newfile.xml but when referencing them from the Java side as
R.integer.myvalue--not found! 

Ended up that I was importing android.R which overrode the expected value
of net.kekeke.narnia.R. 

So that's good to know.
