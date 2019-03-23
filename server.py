import torndb
import tornado.httpserver
import tornado.ioloop
import os
import tornado.web
from tornado.web import RequestHandler
import tornado.options
from binascii import hexlify
from tornado.options import define,options
define("port",default=8000,help="default port ",type=int)
define("mysql_host",default="127.0.0.1:8000")
define("mysqldatabase",default="sr_db")
define("mysqluser",default="root")
define("mysqlpassword",default="13787638")
import mysql.connector


# class Database:
#
#     dbseting={
#         "host":'127.0.0.1',
#         'database':'networkproject',
#         'user':'root',
#         'password':13787638,
#         'charset':'utf8'
#
#     }
#     db=mysql.connector.connect(**dbseting)
#
#
#
#
#     # def insert():


class Aplication(tornado.web.Application):
    def __init__(self):
       handlers =[
           (r'/signup',connect),
           (r'/login\w+',login)
       ]

       setting = dict()
       super().__init__(handlers, **setting)


class BaseHandler(tornado.web.RequestHandler):
    # database=Database.db

    def check_api(self,api):
        result=self.database.get("SELECT * FROM user WHERE api={}".format(api))

    def check_userpass(self,username,password):
        result=BaseHandler.database.get("SELECT * FROM user WHERE username=%s and password=%s ",username,password)





class connect(BaseHandler):
    def post(self):
        output={'status':'200ok'}
        self.write(output)


class login(BaseHandler):
    def post(self):
        output={'status':'oooooooooohhhhhhh'}
        self.write(output)

def main():
    tornado.options.parse_command_line()
    httpserver=tornado.httpserver.HTTPServer(Aplication())
    httpserver.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__=="__main__":
    main()

