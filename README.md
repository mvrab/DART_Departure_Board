# DART Departure Board

A python webpage to display Dallas DART light rail real time arrivals. Real time data is not available through DART GTFS feeds so it is scraped from the mobile website instead.

The code can easily be adapted for any DART rail station.  Finding a train direction relies on knowing the ending destination, so the dart website link as well as destination stations will need to be updated.  For a station as far north as Spring Valley this is simple, since none there are no turn-back points between it and Parker Road.  For other stations with multiple headsigns in both directions, all possible and turn-back points will need to be added to the northbound/southbound if statement.

Designed to be used on a raspberry pi zero inside of an old monitor.  Email mvrablic@mit.edu for a pre-made image intended for use on a Raspberry Pi Zero W.

DART looks to be reevaluating their decision to make the data available to the public, but based on this slide from October 2020, it's unlikely to change soon.
![GTFS-R Slide](https://imgur.com/TSGKiAd.png)
