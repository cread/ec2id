#!/usr/bin/env python

import sys
import urllib

import cherrypy

class EC2InstanceData(object):
    def getData(self, url):
        handle = urllib.urlopen(url)
        data = ""
        if handle.info()["Content-Type"] == "text/plain":
            data = handle.read()
        handle.close()
        return data


    def loadData(self, base, parent=""):
        for key in self.getData(base).split():
            if key.endswith('/'):
                self.loadData(base + key, parent + key)
            else:
                self.keys.append(parent + key)
                self.data[parent + key] = self.getData(base + key)


    def __init__(self):
        self.keys = []
        self.data = {}

        base = "http://169.254.169.254/latest/meta-data/"

        self.loadData(base)


    def index(self):
        res = "<html><head><title>EC2 Instance Data</title></head><body>"
        res += "<h2>EC2 Instance Data:</h2>"
        res += "<table border='1'><tr><th>Key</th><th>Data</th></tr>"

        for key in self.keys:
            res += "<tr><th align='left'>%s</th><td>%s</td></tr>" % (key, self.data[key])

        res += "</table>"
        res += "</body></html>"
        return res

    index.exposed = True


def main(argv):
    cherrypy.config.update({
        'environment': 'production',
        'log.access_file': "/dev/stdout",
        'server.socket_host': "0.0.0.0",
        'server.socket_port': 8080,
        })
    cherrypy.quickstart(EC2InstanceData())


if __name__ == "__main__":
    sys.exit(main(sys.argv))


