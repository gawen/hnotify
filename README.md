# HNotify

``hnotify`` is a little Python script which notifies you when the Hacker News community is active and so when the time is good to send a story on [Hacker News](http://news.ycombinator.com/). This is based on the [Hacker News Story Pickup service](http://hnpickup.appspot.com/).

I didn't program the algorithm, this script is only a UI nutshell upon HNPickup.

Based on [PyQt4](http://wiki.python.org/moin/PyQt4). Works on Linux, MacOSX and Windows.

## Install

The script requires Python (>=2.6), Qt4 for Python (``PySide`` or ``PyQt4``) and ``requests`` for Python.

On Ubuntu,

    apt-get install python-qt4
    pip install requests

Then

    ./hnotify.py

An icon should appear in your systray, notifying you when it's good or bad to send a story.

## About Karma whore-ing

This script **IS NOT** a solution to gain a lot of karma. This is not its aim.

Its primary goal **IS** to let you know when the community is active and when there's not too many messages posted (to avoid being flooded in the mass).

So, to make it simple: **Just post good content and comments, and the karma will take care of itself.**

