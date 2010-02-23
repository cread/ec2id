#!/usr/bin/env python
#   Copyright 2010 Chris Read <chris.read@gmail.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import sys
import urllib
import socket
from optparse import OptionParser

import cherrypy

class EC2InstanceData(object):
    def getData(self, url):
        try:
            handle = urllib.urlopen(url)
            data = ""
            if handle.info()["Content-Type"] == "text/plain":
                data = handle.read()
            handle.close()
            return data
        except:
            return ""


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

        self.base = "http://169.254.169.254/latest/meta-data/"

        self.loadData(self.base)


    def refresh(self):
        self.keys = []
        self.data = {}

        self.loadData(self.base)
        raise cherrypy.HTTPRedirect("/")

    refresh.exposed = True


    def status(self):
        return "All Systems Go"

    status.exposed = True


    def index(self):
        res = "<html><head><title>EC2 Instance Data</title></head><body>"
        res += "<h2>EC2 Instance Data:</h2>"
        res += "<table border='1'><tr><th>Key</th><th>Data</th></tr>"

        for key in self.keys:
            res += "<tr><th align='left'>%s</th><td>%s</td></tr>" % (key, self.data[key])

        res += "</table>"
        res += "<form action='/refresh' method='GET'><input type='submit' value='Refresh'></form>"
        res += "</body></html>"
        return res

    index.exposed = True


def main(argv):
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port", default=8080, type="int",
                      help="Listen on PORT instead of the default of 8080", metavar="PORT")
    parser.add_option("-t", "--timeout", dest="timeout", default=15, type="int",
                      help="Set the default socket timeout value to TIMEOUT seconds instead of the default of 15", metavar="TIMEOUT")

    (options, args) = parser.parse_args()

    socket.setdefaulttimeout(options.timeout)

    cherrypy.config.update({
        'environment': 'production',
        'log.access_file': "/dev/stdout",
        'server.socket_host': "0.0.0.0",
        'server.socket_port': options.port,
        })
    cherrypy.quickstart(EC2InstanceData())


if __name__ == "__main__":
    sys.exit(main(sys.argv))


