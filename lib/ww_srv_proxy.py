#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import signal
import subprocess


class WwSrvProxy:

    def __init__(self, param, mainPort):
        self.param = param
        self.cfgf = os.path.join(self.param.tmpDir, "nginx.cfg")
        self.mainPort = mainPort
        self.surfaceProxyDict = dict()

        self._generateNginxCfgFile()
        self.proc = subprocess.Popen("/usr/sbin/nginx -c %s " % (self.cfgf), shell=True, universal_newlines=True)

    def addSurfaceProxy(self, path, port):
        assert path not in self.surfaceProxyDict

        self.surfaceProxyDict[path] = port
        self._nginxReload()

    def removeSurfaceProxy(self, path):
        del self.surfaceProxyDict[path]
        self._nginxReload()

    def dispose(self):
        self.proc.terminate()
        self.proc.wait()
        self.proc = None

    def _generateNginxCfgFile(self):
        buf = ""
        buf += "daemon off;\n"
        buf += "\n"
        buf += "events {\n"
        buf += "}\n"
        buf += "\n"
        buf += "http {\n"
        buf += "    server {\n"
        buf += "        listen 80;\n"
        buf += "        location / {\n"
        buf += "            proxy_pass http://localhost:%d;\n" % (self.mainPort)
        buf += "        }\n"
        for path, port in self.surfaceProxyDict.items():
            buf += "        location /surface/%s {\n" % (path)
            buf += "            proxy_pass http://localhost:%d;\n" % (port)
            buf += "        }\n"
        buf += "    }\n"
        buf += "}\n"
        with open(self.cfgf, "w") as f:
            f.write(buf)

    def _nginxReload(self):
        self._generateNginxCfgFile()
        self.proc.send_signal(signal.SIGHUP)
