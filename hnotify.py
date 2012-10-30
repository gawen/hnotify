#!/usr/bin/env python

__author__ = "Gawen Arab"
__copyright__ = "Copyright 2012, Gawen Arab"
__credits__ = ["Gawen Arab"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Gawen Arab"
__email__ = "gawen@forgetbox.com"
__status__ = "Beta"

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import urllib
import json
import time
import os
import sys
import webbrowser
import logging

local_path = os.path.dirname(__file__)

logger = logging.getLogger("hnotify")

def get_state():
    logger.info("Getting state...")
    ndata_elements = 3
    try:
        quantiles = json.loads(urllib.urlopen("http://hnpickup.appspot.com/dm.json?ndata_elements=%s" % (1, )).read())[0]
        
        series = json.loads(urllib.urlopen("http://hnpickup.appspot.com/etl.json?ndata_elements=%s" % (ndata_elements, )).read())

    except IOError:     # Can't connect
        logger.warning("Looks like HNPickup is down or no connectivity.")
        return "offline"

    except ValueError:  # Bad JSON
        logger.warning("Bad JSON returned.")
        return "offline"

    stories = series.pop()
    data_length = len(series[0]["data"]) - 1
    timing_diff = series[2]["data"][data_length][1]
    
    if timing_diff > quantiles["quant1"]:
        return "very good"

    elif timing_diff > quantiles["quant2"]:
        return "good"

    elif timing_diff > quantiles["quant3"]:
        return "so-so"

    else:
        return "bad"

class MainWindow(QMainWindow):
    TIMER_LAPS = 15 * 60 * 1000

    def __init__(self):
        super(MainWindow, self).__init__()

        self.last_sugg = None

        self.icon_verygood = QIcon(os.path.join(local_path, "icon-verygood.ico"))
        self.icon_good = QIcon(os.path.join(local_path, "icon-good.ico"))
        self.icon_soso = QIcon(os.path.join(local_path, "icon-soso.ico"))
        self.icon_bad = QIcon(os.path.join(local_path, "icon-bad.ico"))
        self.icon_offline = QIcon(os.path.join(local_path, "icon-offline.ico"))

        self.refresh_contextmenu_action = QAction("Refresh now", self)
        self.connect(self.refresh_contextmenu_action, SIGNAL("triggered()"), lambda: self.update_pickup(True))

        self.visit_pickup_contextmenu_action = QAction("Visit HN Pickup", self)
        self.connect(self.visit_pickup_contextmenu_action, SIGNAL("triggered()"), self.visit_pickup_website)

        self.visit_hn_contextmenu_action = QAction("Visit HN", self)
        self.connect(self.visit_hn_contextmenu_action, SIGNAL("triggered()"), self.visit_hn_website)
        
        self.quit_contextmenu_action = QAction("Quit", self)
        self.connect(self.quit_contextmenu_action, SIGNAL("triggered()"), self.quit)

        self.menu = QMenu()
        self.menu.addAction(self.refresh_contextmenu_action)
        self.menu.addSeparator()
        self.menu.addAction(self.visit_hn_contextmenu_action)
        self.menu.addAction(self.visit_pickup_contextmenu_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_contextmenu_action)

        self.tray = QSystemTrayIcon(self.icon_bad, self)
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        self.connect(self.tray, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.on_tray)

        self.timer = QTimer()
        self.connect(self.timer, SIGNAL("timeout()"), self.update_pickup)
        self.timer.start(self.TIMER_LAPS)

        self.update_pickup()

    def update_pickup(self, force_display = None):
        force_display = force_display if force_display is not None else False

        self.tray.setIcon(self.icon_bad)

        try:
            sugg = get_state()

        except:
            import traceback
            traceback.print_exc()
            return

        if not force_display and self.last_sugg == sugg:
            return

        icon, message, timer_laps = {
            "very good": (self.icon_verygood, "Very-good time to post on HN.", None),
            "good": (self.icon_good, "Good time to post on HN.", None),
            "so-so": (self.icon_soso, "So-so time to post on HN.", None),
            "bad": (self.icon_bad, "Bad time to post on HN.", None),
            "offline": (self.icon_offline, "Offline", 30 * 1000),

        }.get(sugg, self.icon_bad)

        self.tray.setIcon(icon)
        self.timer.setInterval(timer_laps or self.TIMER_LAPS)
        self.tray.showMessage("Hacker News", message)
        
        self.last_sugg = sugg
            
    def on_tray(self, reason):
        if reason != QSystemTrayIcon.Trigger:
            return

        self.update_pickup(True)
    
    def visit_hn_website(self):
        webbrowser.open("http://news.ycombinator.com/")

    def visit_pickup_website(self):
        webbrowser.open("http://hnpickup.appspot.com/")

    def quit(self):
        QApplication.quit()

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig()

    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
