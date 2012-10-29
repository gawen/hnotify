#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import requests
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
    quantiles = requests.get("http://hnpickup.appspot.com/dm.json?ndata_elements=%s" % (1, )).json[0]

    series = requests.get("http://hnpickup.appspot.com/etl.json?ndata_elements=%s" % (ndata_elements, )).json

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
    def __init__(self):
        super(MainWindow, self).__init__()

        self.last_sugg = None

        self.icon_verygood = QIcon(os.path.join(local_path, "icon-verygood.png"))
        self.icon_good = QIcon(os.path.join(local_path, "icon-good.png"))
        self.icon_soso = QIcon(os.path.join(local_path, "icon-soso.png"))
        self.icon_bad = QIcon(os.path.join(local_path, "icon-bad.png"))

        self.tray = QSystemTrayIcon(self.icon_bad, self)
        self.tray.show()
        self.connect(self.tray, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.on_tray)

        self.timer = QTimer()
        self.connect(self.timer, SIGNAL("timeout()"), self.update_pickup)
        self.timer.start(5 * 60 * 1000)

        self.update_pickup()

    def update_pickup(self):
        try:
            sugg = get_suggestion()

        except:
            import traceback
            traceback.print_exc()
            return

        if self.last_sugg == sugg:
            return

        icon = {
            "very good": self.icon_verygood,
            "good": self.icon_good,
            "so-so": self.icon_soso,
            "bad": self.icon_bad,
        }.get(sugg, self.icon_bad)

        self.tray.setIcon(icon)
        
        self.tray.showMessage("Hacker News", "%s time to post on HN." % (sugg.capitalize(), ))
        
        self.last_sugg = sugg

    def on_tray(self):
        webbrowser.open("http://hnpickup.appspot.com/")
    
def main():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig()

    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
