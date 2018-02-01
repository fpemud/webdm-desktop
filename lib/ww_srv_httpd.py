#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import cherrypy
from ww_util import WwUtil


class WwSrvHttpd:

    def __init__(self, param):
        self.param = param
        self.port = WwUtil.getFreeSocketPort("tcp")

        from cherrypy._cpnative_server import CPHTTPServer
        cherrypy.server.socket_host = "127.0.0.1"
        cherrypy.server.socket_port = self.port
        cherrypy.server.httpserver = CPHTTPServer(cherrypy.server)

        cherrypy.tree.mount(Root(), config={
            "/": {
                "tools.staticdir.on": True,
                "tools.staticdir.dir": self.param.wwwDir,
                "tools.staticdir.index": "index.html",
            },
        })
        cherrypy.engine.start()

    def getPort(self):
        return self.port

    def dispose(self):
        cherrypy.engine.stop()


class Root(object):
    pass
