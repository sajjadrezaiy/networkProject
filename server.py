# import torndb
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
import re


class Database:
    DATABASE_ = mysql.connector.connect(host='localhost', database='network', user='root', password='s@mba123@li14')








class Aplication(tornado.web.Application):
    def __init__(self):
       handlers =[
           (r'/signup',connect),
           (r'/login.*',login),
           (r"/logout.*",logout),
           (r'/sendticket.*',sendticket)

       ]

       setting = dict()
       super().__init__(handlers, **setting)


class BaseHandler(tornado.web.RequestHandler):
    # database=Database.db

    def check_api(self,api):
        result=self.database.get("SELECT * FROM user WHERE api={}".format(api))

    def check_userpass(self,username,password):
        result=BaseHandler.database.get("SELECT * FROM user WHERE username=%s and password=%s ",username,password)

    def check_user(self,username):
        result=BaseHandler.database.get("SELECT * FROM net WHERE username=%s ",username)





class DefaultHandler(BaseHandler):
    def get(self):
        output={'status':'404 not found'}
        self.write(output)

    def post(self):
        output={'status':'404 not found'}
        self.write(output)

class connect(BaseHandler):
    def post(self):
        output={'status':'200ok'}
        self.write(output)


class login(BaseHandler):
    def post(self):
        output={'status':'oooooooooohhhhhhh','id':'sajjad'}
        self.write(output)

class logout(BaseHandler):
    # db=Database.DATABASE_
    def post(self,*args,**kwargs):
        username=self.get_argument('username')
        print("hellow ",username)
        password=self.get_argument('password')
        print('your passowod is',password)

        output={username:password}
        self.write(output)

        # else:
            # logout.db.execute("DELETE from potluck  where name='%s';",args[0])


class sendticket(BaseHandler):
    database=Database.DATABASE_
    def get(self,*args,**kwargs):
        token=self.get_argument('token')
        subject=self.get_argument('subject')
        body=self.get_argument('body')

        if  not self.check_api(token):
            output={"staus":"this token not found"}
            self.write(output)

        else:
            sendticket.database.execute("INSERT IN TO ticket (token,subject,body)" "values (%s,%s,%s)",token,subject,body)




def main():
    tornado.options.parse_command_line()
    httpserver=tornado.httpserver.HTTPServer(Aplication())
    httpserver.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__=="__main__":
    main()

