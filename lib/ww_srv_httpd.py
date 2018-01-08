#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import cherrypy


class WwHttpd:

    def __init__(self, param):
        self.param = param
        cherrypy.tree.mount(Root(), config={
            "/": {
                "tools.staticdir.on": True,
                "tools.staticdir.dir": self.param.wwwDir,
                "tools.staticdir.index": "index.html",
            },
        })
        cherrypy.engine.start()

    def dispose(self):
        cherrypy.engine.stop()


class Root(object):
    pass
