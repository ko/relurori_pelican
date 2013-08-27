Title: Native Glass, Sensors pt. 1
Date: 2013/07/24
Tags: google glass, sensors, android 
Author: Ken Ko

Unlike previous posts, there are no code samples here. 

Looks like there are two issues I'm faced with, at the moment. 

1. Google Play Store is not installed
2. GPS location updates rely on MyGlass

Without the Google Play library, Google Maps is a no-go. 
Without GPS location updates, accurate position data is a no-go.

To mitigate the Google Play Store, we can try out OpenStreetMaps, or even 
try to add Google App Suite to the Glass. Don't know how either would fly, 
at the moment, but I have a hunch that OSM would be the better path to at 
least investigate initially. 

Regarding GPS location, I think one path would be to decompile MyGlass and 
see how it's forwarding the Navigation app information/view to the Glass unit.

Realistically, I have setup bluetooth data sharing between my Galaxy
Nexus and Google Glass where the infrastructure is setup to 
straightforwardly transmit GPS coordinates (or even byte streams) from 
phone to Glass. 

Should be able to add code samples sometime in the future, time 
prohibiting.
