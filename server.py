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



class Database:

    dbseting={
        "host":'options.mysql_host',
        'database':'options.mysqldatabase',
        'user':'options.mysqkyser',
        'password':'options.mysqlpassword',
        'charset':'utf8'

    }
    db=torndb.Connection(**dbseting)



    def insert():



class BaseHandler(tornado.web.RequesHandler):
    database=Database.db

    def check_api(self,api):
        result=self.database.get("SELECT * FROM user WHERE api={}".format(api))

    def check_userpass(self,username,password):
        result=BaseHandler.database.get("SELECT * FROM user WHERE username=%s and password=%s ",username,password)


