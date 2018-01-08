#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os


class WwParam:

    def __init__(self):
        self.libDir = "/usr/lib/webwin"
        self.shareDir = "/usr/share/webwin"
        self.runDir = "/run/webwin"
        self.logDir = "/var/log/webwin"
        self.tmpDir = "/tmp/webwin"
        self.varDir = "/var/webwin"

        self.mainloop = None

        self.pidFile = os.path.join(self.runDir, "webwin.pid")
        self.wwwDir = os.path.join(self.shareDir, "www")
        self.logLevel = None
        self.config = None

        self.srvProxy = None
        self.srvHttpd = None

