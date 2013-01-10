"""A specialized :class:`pulsar.apps.socket.SocketServer` for
serving web applications which conforms with the python web server
gateway interface (WSGI_).

The application can be used in conjunction with several web frameworks
as well as the :ref:`pulsar RPC middleware <apps-rpc>` and
the :ref:`websocket middleware <apps-ws>`.

An example of a web server written with ``pulsar.apps.wsgi`` which responds
with "Hello World!" for every request::

    from pulsar.apps import wsgi

    def hello(environ, start_response):
        data = b"Hello World!"
        response_headers = (
            ('Content-type','text/plain'),
            ('Content-Length', str(len(data)))
        )
        start_response("200 OK", response_headers)
        return [data]

    if __name__ == '__main__':
        wsgi.WSGIServer(callable=hello).start()


For more information regarding WSGI check the pep3333_ specification.

.. _pep3333: http://www.python.org/dev/peps/pep-3333/
.. _WSGI: http://www.wsgi.org
"""
from functools import partial

import pulsar
from pulsar.apps.socket import SocketServer

from .wsgi import *
from .server import *
from .middleware import *


class HttpParser(pulsar.Setting):
    app = 'wsgi'
    section = "WSGI Servers"
    name = "http_parser"
    flags = ["--http-parser"]
    desc = """\
        The HTTP Parser to use. By default it uses the fastest possible.

        Specify `python` if you wich to use the pure python implementation
        """


class WSGIServer(SocketServer):
    cfg_apps = ('socket',)
    _app_name = 'wsgi'

    def handler(self):
        '''Build a :class:`WsgiHandler` for the WSGI callable provided
and return an :class:`HttpResponse` factory function.'''
        if not isinstance(self.callable, WsgiHandler):
            if not isinstance(hnd, (list, tuple)):
                hnd = [hnd]
            self.callable = WsgiHandler(hnd)
        return partial(HttpServerResponse, self.callable)