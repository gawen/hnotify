# HNotify

``hnotify`` is a little Python script which notifies you when it's good time to send a story on [Hacker News](http://news.ycombinator.com/). This is based on the [Hacker News Story Pickup service](http://hnpickup.appspot.com/).

Based on [PyQt4](http://wiki.python.org/moin/PyQt4). Works on Linux, MacOSX and Windows.

## Install

The script requires Python (>=2.6), Qt4 for Python (``PySide`` or ``PyQt4``) and ``requests`` for Python.

On Ubuntu,

    apt-get install python-qt4
    pip install requests

Then

    ./hnotify.py

An icon should appear in your systray, notifying you when it's good or bad to send a story.
