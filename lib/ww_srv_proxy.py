#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import signal
import subprocess
from ww_util import WwUtil


class WwSrvProxy:

    def __init__(self, param, mainPort):
        self.param = param

        self.cfgf = os.path.join(self.param.tmpDir, "nginx.cfg")
        self.keySize = 1024
        self.caCertFile = os.path.join(self.param.varDir, "ca-cert.pem")
        self.caKeyFile = os.path.join(self.param.varDir, "ca-privkey.pem")
        self.servCertFile = os.path.join(self.param.varDir, "server-cert.pem")
        self.servKeyFile = os.path.join(self.param.varDir, "server-privkey.pem")

        self.mainPort = mainPort
        self.surfaceProxyDict = dict()

        self._generateCertAndKey()
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
        buf += "    auth_pam              \"Please specify login and password\";\n"
        buf += "    auth_pam_service_name \"webwin\";\n"
        buf += "    server {\n"
        buf += "        listen              443 ssl;\n"
        buf += "        ssl_certificate     %s;\n" % (self.servCertFile)
        buf += "        ssl_certificate_key %s;\n" % (self.servKeyFile)
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

    def _generateCertAndKey(self):
        if os.path.exists(self.servCertFile) and os.path.exists(self.servKeyFile):
            return

        if not os.path.exists(self.caCertFile) or not os.path.exists(self.caKeyFile):
            caCert, caKey = WwUtil.genSelfSignedCertAndKey("default", self.keySize)
            WwUtil.dumpCertAndKey(caCert, caKey, self.caCertFile, self.caKeyFile)
        else:
            caCert, caKey = WwUtil.loadCertAndKey(self.caCertFile, self.caKeyFile)

        cert, k = WwUtil.genCertAndKey(caCert, caKey, "default", self.keySize)
        WwUtil.dumpCertAndKey(cert, k, self.servCertFile, self.servKeyFile)
