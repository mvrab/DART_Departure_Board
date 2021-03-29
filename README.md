# DART Departure Board

![Departure board](https://i.imgur.com/i4VNMQb.jpg)

A python webpage to display Dallas DART light rail real time arrivals. Real time data is not available through DART GTFS feeds so it is scraped from the mobile website instead.

The code can easily be adapted for any DART rail station.  Finding a train direction relies on knowing the ending destination, so the dart website link as well as destination stations will need to be updated depending on the station used.  For a station as far north as Spring Valley this is simple, since there are no turn-back points between it and Parker Road.  For other stations with multiple headsigns in both directions, all possible and turn-back points will need to be added to the northbound/southbound if statement.

Designed to be used on a raspberry pi zero inside of an old 1280*1024 monitor.  A pre-made image intended for use on a Raspberry Pi Zero W is [available here](https://mega.nz/file/6Y4gnRBS#twmQj192V3xVO4861dGGzrvbwmWZjWNNBRejZXfcxPE).  To use it, flash the image onto an 8gb or larger SD, plug the sd into any Windows, Mac, or Linux PC.  Edit wpa_supplicant.conf in the boot partition with your wifi network name and password.  If desired, expand the partition to fill the SD, but this is not necessary for normal operation.  Startup is slow, taking ~2 minutes.  All logging and swapping has been disabled to preserve the SD card, and an automatic reboot is scheduled every night at 4:00am.  The default username is "pi" and password "dartdisplay".  SSH is enabled so change the password after first boot for higher security.

DART looks to be reevaluating their decision to make the data available to the public, but based on this slide from October 2020, it's unlikely to change soon.
![GTFS-R Slide](https://imgur.com/TSGKiAd.png)
