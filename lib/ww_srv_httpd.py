#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import cherrypy
from ww_util import WwUtil


class WwSrvHttpd:

    def __init__(self, param):
        self.param = param
        self.port = WwUtil.getFreeSocketPort("tcp")
        self.root = Root()

        from cherrypy._cpnative_server import CPHTTPServer
        cherrypy.server.socket_host = "127.0.0.1"
        cherrypy.server.socket_port = self.port
        cherrypy.server.httpserver = CPHTTPServer(cherrypy.server)

        cfgDict = dict()
        cfgDict["/"] = {
            "tools.staticdir.root": self.param.wwwDir,
        }
        cfgDict["/index.html"] = {
        }
        cfgDict["/common"] = {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "./common",
        }
        cfgDict["/api"] = {
        }
        for fn in os.listdir(os.path.join(self.param.wwwDir, "pages")):
            cfgDict["/pages/%s/%s.html" % (fn)] = {
            }
            if os.path.exists(os.path.join(self.param.wwwDir, "pages", "css")):
                cfgDict["/pages/%s/css" % (fn)] = {
                    "tools.staticdir.on": True,
                    "tools.staticdir.dir": "./pages/%s/css" % (fn),
                }
            if os.path.exists(os.path.join(self.param.wwwDir, "pages", "images")):
                cfgDict["/pages/%s/images" % (fn)] = {
                    "tools.staticdir.on": True,
                    "tools.staticdir.dir": "./pages/%s/images" % (fn),
                }
            if os.path.exists(os.path.join(self.param.wwwDir, "pages", "js")):
                cfgDict["/pages/%s/js" % (fn)] = {
                    "tools.staticdir.on": True,
                    "tools.staticdir.dir": "./pages/%s/js" % (fn),
                }
            cfgDict["/api/"] = {
            }
        cherrypy.tree.mount(self.root, config=cfgDict)

        cherrypy.engine.start()

    def getPort(self):
        return self.port

    def dispose(self):
        cherrypy.engine.stop()


class Root(object):
    pass


@cherrypy.expose
class Surfaces(object):

    def __init__(self):
        self.childDict = dict()

    def _cp_dispatch(self, vpath):
        if len(vpath) >= 1:
            surfaceName = vpath.pop()
            if surfaceName in self.childDict:
                return self.childDict[surfaceName]
        return vpath


@cherrypy.expose
class Surface(object):

	def __init__(self, content):
		self.content = content
        self.childDict = dict()

	def GET(self):
		return self.to_html()

	def POST(self):
		self.content = self.from_html(cherrypy.request.body.read())

	def to_html(self):
		html_item = lambda (name,value): '<div>{name}:{value}</div>'.format(**vars())
		items = map(html_item, self.content.items())
		items = ''.join(items)
		return '<html>{items}</html>'.format(**vars())

	@staticmethod
	def from_html(data):
		pattern = re.compile(r'\<div\>(?P<name>.*?)\:(?P<value>.*?)\</div\>')
		items = [match.groups() for match in pattern.finditer(data)]
		return dict(items)