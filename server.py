import torndb
import tornado.httpserver
import tornado.ioloop
import os
import tornado.web
from tornado.web import RequestHandler
import tornado.options
from binascii import hexlify
from tornado.options import define,options
define("port",default=1104,help="default port ",tuple=int)
define("mysql_host",default="127.0.0.1:8000")
define("mysqldatabase",default="sr_db")
define("mysqluser",default="root")
define("mysqlpassword",default="toor")



class BaseHandler(tornado.web.RequesHandler):
    