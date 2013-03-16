
RadioX
======

 - by Rob Cakebread <cakebread@gmail.com>

The goal of the RadioX project is to make an easily deployable, fully
featured internet radio station with live on-air conferencing requiring
no special hardware - callers dial in with regular phones.

RadioX will act as a SIP or Google Voice endpoint and use Twilio and 
Freeswitch for conference calls and purchasing phone numbers.

With the included Cuisine fab file and Vagrant, you can be up and streaming 
in a dev box with Airtime in minutes.

The public facing website for displaying show schedules and what
is currently being played is powered by Django, Mezzanine and
Bootstrap for a modern look and feel in browsers and on phones.

Airtime can be used for the back-end web interface to schedule shows by DJs 
and station managers. If you don't need scheduling, RadioX can simply play 
random songs or be controlled by any mpd client. This mode allows DJing 
from phones without show interruptions from dropped cell or wifi 
connections. The media is stored on the RadioX server in this mode.

Whether you use Airtime or your own input method, the stream is 
mastered by Liquidsoap. Liquidsoap is a functional programming 
language developed to mix audio sources and stream to an Icecast2 
or Shoutcast server. Liquidsoap is written in oCaml.

RadioX can be put into request mode where listeners cand send SMS
text messages or Jabber IMs to search for and request songs.

I would love to develop a Django front-end for Airtime to be an alternate
front-end for the existing php one that comes with it and contribute
it back to Airtime, if they wish. This is low priority, as the php one 
works great, it would just be a pleasure to hack on a Python front-end.

Ok, this is "README-driven" development, so these features aren't all 
implemented yet, but here is what you can do today with the Cuisine fab file:

 * Install an Ubuntu 12.04 system on a VirtualBox locally via Vagrant with a 
 running Airtime installation, already streaming music.

 * A Django / Mezzanine app installed locally ready to set up with show 
 schedules, current playing info live from the stream, etc.
 


Installation
------------

To get a fully functioning radio station streaming on port 9999 on
your local Linux box using Vagrant:

    Inside a Python virtualenv:

    $ clone git://github.com/cakebread/radiox.git && cd radiox
    $ vagrant up
    $ fab vagrant setup

    Now check it out:

    $ mplayer http://localhost:9999/airtime_128 # Icecast ogg stream
    $ firefox http://localhost:9080  # Airtime web interface

A few sample songs are in the library and your radio station is now
streaming music!

See this article to learn about the master source and show source:
http://en.flossmanuals.net/airtime-en-2-2/stream-settings/

You can have multiple Djs with separate passwords, only able to connect 
to the stream during their scheduled shows, or station managers who 
can connect any time and over-ride the stream, etc.


Listening and Scheduling
------------------------

Accessing the Radio Staion running in the Vagrant VirtualBox:

    Stream:

        http://localhost:9999/airtime_128
        (Icecast2 URL for phones, media players etc.)

    Airtime Admin Web Interface for Djs :

        http://localhost:9080   (Airtime admin interface)


