#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import sys
import json
import signal
import shutil
import logging
import toposort
import netifaces
from gi.repository import GLib
from gi.repository import GObject
from ww_util import WwUtil


class WwDaemon:

    def __init__(self, param):
        self.param = param

    def run(self):
        WrtUtil.mkDirAndClear(self.param.tmpDir)
        WrtUtil.mkDirAndClear(self.param.runDir)
        try:
            logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))
            logging.getLogger().setLevel(WrtUtil.getLoggingLevel(self.param.logLevel))
            logging.info("Program begins.")

            # write pid file
            with open(self.param.pidFile, "w") as f:
                f.write(str(os.getpid()))

            # create main loop
            self.param.mainloop = GLib.MainLoop()

            # business initialize
            self.param.srvHttpd = WwHttpd()
            self.param.srvProxy = WwProxy()

            # start main loop
            logging.info("Mainloop begins.")
            GLib.unix_signal_add(GLib.PRIORITY_HIGH, signal.SIGINT, self._sigHandlerINT, None)
            GLib.unix_signal_add(GLib.PRIORITY_HIGH, signal.SIGTERM, self._sigHandlerTERM, None)
            self.param.mainloop.run()
            logging.info("Mainloop exits.")
        finally:
            if self.param.srvProxy is not None:
                self.param.srvProxy.dispose()
            if self.param.srvHttpd is not None:
                self.param.srvHttpd.dispose()
            logging.shutdown()
            shutil.rmtree(self.param.runDir)
            shutil.rmtree(self.param.tmpDir)

    def _sigHandlerINT(self, signum):
        logging.info("SIGINT received.")
        self.param.mainloop.quit()
        return True

    def _sigHandlerTERM(self, signum):
        logging.info("SIGTERM received.")
        self.param.mainloop.quit()
        return True
