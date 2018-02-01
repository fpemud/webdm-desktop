#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-


class WwProxy:

    def __init__(self, param):
        self.param = param
        self.tmpDir = os.path.join(self.param.tmpDir, "proxy")

    def start(self):
        cfgf = os.path.join(self.tmpDir, "config.ovpn")

        # run nginx process
        cmd = ""
        cmd += "/usr/sbin/nginx "
        cmd += "-c %s " % (cfgf)
        cmd += "--writepid %s/openvpn.pid " % (self.tmpDir)
        cmd += "> %s/openvpn.out 2>&1" % (self.tmpDir)
        self.proc = subprocess.Popen(cmd, shell=True, universal_newlines=True)


        pass

    def stop(self):
        pass



