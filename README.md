# MusicPlayer
Simple Music Player application including GPIO and web (created with Python3 and Tornado) interface

At its origin, application was intented to be serving as a music player. With development, I decided to make it play radio streams. Due to the fact, that it was a part of _Linux in Embedded Systems_ cource's assignment, and it was developed under pressure of time, list of available streams is hard-coded in the MusicPlayer class. If you want to specify your own streams/tracks, just edit that list and, if you want to add some own tracks, place them in the `/var/lib/mpd/music` directory.

Mind the fact, that GPIO pins are also hard-coded. However, it can be easily changed to your own preferences in the GPIOController class file. Every single LED indicates a specific radio station being played, and buttons allow to:

* increase/decrease volume (LEFT and RIGHT buttons),
* change streams (LEFT and RIGHT buttons with TOP button pressed),
* play/pause player (TOP button).

Branch `lab05` contains version with own GPIOController implementation (with no use of `RPi.GPIO` package). It is quite less efficient, but it allows to use `MusicPlayer` with LEDE Project precompiled image, with no need to add RPi.GPIO manually with SDK.
