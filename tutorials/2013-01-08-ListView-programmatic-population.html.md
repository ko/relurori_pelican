Title: Android ListView, programmatic population
Date: 2013/01/08 20:45
Author: Ken Ko
Tags: android

Apart from statically declaring things in the R.layout.yourActivity.xml
file, it's nice to also have a dynamic method for populating a ListView. 

It's been useful for testing, but now that I have a basic RESTful API up
and running on my webserver there's no need for dummy data.

<code>
ListView myListRecent;
String[] myArray;
ArrayAdapter<String> adapter;

// Setup the wish list array of strings
myArray = new String[5];
myArray[0] = "Hello";
myArray[1] = "World";
myArray[2] = "";
myArray[3] = "Goodbye";
myArray[4] = "Self";

// ArrayAdapter bridging the ListView and String[]
adapter = new ArrayAdapter<String>(this, 
                                   android.R.layout.simple_list_item_1, 
                                   myArray);

myListRecent = (ListView) findViewById(R.id.wish_list_recent);
myListRecent.setAdapter(adapter);
</code>

Posting this as reference, for the most part.
