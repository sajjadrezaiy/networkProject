import torndb
import tornado.httpserver
import tornado.ioloop
import os
import tornado.web
from tornado.web import RequestHandler
import tornado.options
from binascii import hexlify
from tornado.options import define, options

define("port", default=8000, help="default port ", type=int)
define("mysql_host", default="127.0.0.1:8000")
define("mysqldatabase", default="sr_db")
define("mysqluser", default="root")
define("mysqlpassword", default="13787638")
import mysql.connector
import re
from datetime import date
import secrets


class Database:
    DATABASE_ = torndb.Connection(host='localhost', database='network', user='root', password='s@mba123@li14')
    modir_token=DATABASE_.query("select * from net where id=%d",0)



class Aplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/signup', connect),
            (r'/login.*', login),
            (r'/signup*',signup),
            (r"/logout.*", logout),
            (r'/sendticket.*', sendticket)
            (r'/postticket.*',getticket)
            (r'/closeticket.*',closeticket)
            (r'/restoticketmod.*',restoticketmod)
            (r'changestatus.*',changestatus)
        ]

        setting = dict()
        super().__init__(handlers, **setting)


class BaseHandler(tornado.web.RequestHandler):
    database=Database.db
    modir_token=Database.modir_token

    def check_api(self, api):
        result = BaseHandler.database.query("SELECT * FROM user WHERE token={}".format(api))
        if result:
            return True
        else:
            return False
    def check_modir_api(self,api):
        result=BaseHandler.database.query("select * from net where token=%s",BaseHandler.modir_token)
        if result:
            return True
        else:
            return False

    def check_userpass(self, username, password):
        result = BaseHandler.database.query("SELECT * FROM user WHERE username=%s and password=%s ", username, password)
        if result:
            return True
        else:
            return False

    def check_user(self, username):
        result = BaseHandler.database.query("SELECT * FROM net WHERE username=%s ", username)
        if result:
            return True
        else:
            return False


class DefaultHandler(BaseHandler):
    def get(self):
        output = {'status': '404 not found'}
        self.write(output)

    def post(self,*args,**kwargs):
        output = {'status': '404 not found'}
        self.write(output)


class connect(BaseHandler):
    def post(self):
        output = {'status': '200ok'}
        self.write(output)

class login(BaseHandler):
    db=Database.DATABASE_
    def post(self):
        username=self.get_argument('username')
        password=self.get_argument('password')
        if self.check_user(username):
            token=login.db.query("select * from ticket where username=%s", username)[0]['token']
            output={"message": "Logged in Successfully","code": "200","token":token}
            self.write(output)
        else:
            output={"message":"user not exist ","code":"404"}
            self.write(output)
    def get(self,*args):
        username=args[0]
        password=args[1]
        if self.check_user(username):
            token=login.db.query("select * from ticket where username=%s", username)[0]['token']
            output={"message": "Logged in Successfully","code": "200","token":token}
            self.write(output)
        else:
            output={"message":"user not exist ","code":"404"}
            self.write(output)
class logout(BaseHandler):
    def post(self):
        username=self.get_argument('username')
        password=self.get_argument('password')
        if self.check_userpass(username):
            output={"message": "Logged Out Successfully", "code": "200"}
            self.write(output)
        else:
            output={"status":"username or password is wrong","code":"200"}
            self.write(output)

    def get(self,*args):
        username=args[0]
        password=args[1]
        if self.check_userpass(username,password):
            output={"message":"logout successfully","code":"200"}
            self.write(output)
        else:
            output={"status":"username or password is worng","code":"200"}
            self.write(output)


class signup(BaseHandler):
    def get(self,*args):
        if len(*args==2):
            username = args[0]
            password =  args[1]

        if not self.check_user(username):
            token = secrets.token_hex(16)
            if len(*args>2):
                firstname = args[2]
            else:
                firstname = None
            if len(*args==4):
                lastname = args[3]
            else:
                lastname = None
            result = signup.db.execute("INSERT INTO net (username,password,token,firstname,lastname)" "values (%s,%s,%s,%s)", username, password,token, firstname, lastname)
            output = {"api": token, 'status': 'ok'}
            self.write(output)

        else:
            output = {"status": "user exist"}
            self.write(output)

    def post(self):
        username=self.get_argument('username')
        password=self.get_argument('password')
        if not self.check_user(username):
            token=secrets.token_hex(16)
            if self.get_argument('firstname'):
                firstname=self.get_argument('firstname')
            else:
                firstname=None
            if self.get_argument('lastname'):
                lastname=self.get_argument('lastname')
            else:
                lastname=None
            result=signup.db.execute("INSERT INTO net (username,password,token,firstname,lastname)" "values (%s,%s,%s,%s)", username,password,token,firstname,lastname)
            output={"api":token,'status':'ok'}
            self.write(output)

        else:
            output={"status":"user exist"}
            self.write(output)



class sendticket(BaseHandler):
    database = Database.DATABASE_
    cdate=str(date.today())

    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        subject = self.get_argument('subject')
        body = self.get_argument('body')

        if not self.check_api(token):
            output = {"staus": "this token not found"}
            self.write(output)

        else:

            sendticket.database.execute("INSERT INTO ticket (token,subject,body,cdate)" "values (%s,%s,%s,%s)", token, subject, body,sendticket.cdate)

            user = sendticket.database.query("select * from ticket where token=%s", token)
            output = {'message': 'ticket sent success fully', 'id': id, 'code': '200'}
            id = len(user)
            output = {'message': 'ticket sent success fully', 'id':id, 'code': '200'}
            self.write(output)

class getticket(BaseHandler):
    db=Database.DATABASE_

    def post(self):
        token = self.get_argument('token')
        if not self.check_api(token):

            output={'status':'404 this token not found'}
        else:
             user = getticket.db.query("select * from ticket where token=%s", token)

             mainid = user[len(user) - 1]['id']
             id = len(user)
             subject = user[id - 1]['subject']
             body = user[id - 1]['body']
             status = user[id - 1]['state']
             cdate = user[id - 1]['cdate']

             output = {'ticket': 'tere are -%d-ticket' % id, 'code': '200',
              'block %d' % (id - 1): {"subject": '%s' % subject, "body": '%s' % body, "status": '%s' % status,
                                      "id": '%d' % id, "date": '%s' % cdate}}

             self.write(output)

class closeticket(BaseHandler):
    db=Database.DATABASE_
    modir_token =Database.modir_token

    def post(self):
        token=self.get_argument('token')
        id=self.get_argument('id')
        if (token!=closeticket.modir_token):
            output={"status":"you don't have permiton to close the ticket"}
        if (not self.check_api(token)):
            output={"status":"404 ths token not found"}

        else:

            user=closeticket.db.query("select * from ticket where token=%s",token)
            id_=user[len(user)-1]['id']
            state = 'close'
            if id!=id_:
                output={"message":"this id not found"}
                self.write(output)
            else:
                closeticket.db.execute("update ticket set state=%s where token=%s", state, token)
                output={"message":"ticket with id -%s- closed successfully"%str(id),"code":"200"}
                self.write(output)
#########*****> def get

class getticketmod(BaseHandler):
    db=Database.DATABASE_
    modir_token =db.query("select * from net where id=%d", 0)

    def post(self):
        token=self.get_argument('token')
        if not self.check_api(token) and token!=getticketmod.modir_token:
            output={"status":"404 this token not found"}
        if token==getticketmod.modir_token:
                self.write(output)
                state = 'open'
                user = getticketmod.db.query("select * from ticket where state=%s ", state)
                numticket = len(user)

                output={"ticket":"ther are -%d- ticket"%numticket,"code":"200"}

                counter=0
                for i in range(0, len(user)):
                    subject = user[counter]['subject']
                    body = user[counter]['body']
                    status = user[counter]['state']
                    id = user[counter]['id']
                    cdate = user[counter]['cdate']
                    extoutput = {
                        "block %d" % counter: {"subject": '%s' % subject, "body": '%s' % body, "status": '%s' % status,
                                               "date": '%s' % cdate}}

                    output.update(extoutput)
                    counter = counter + 1
        else:
            output={"you don't have permiton to see the ticekt"}
        self.write(output)
#####**********>>>>>get



class restoticketmod(BaseHandler):
    db=Database.DATABASE_
    def pos(self):
        token_modir=self.get_argument('token')
        if  self.check_api(token_modir):
           if not self.check_modir_api(token_modir):
               output={"status":"permition denied"}
               self.write(output)
        if not self.check_api(token_modir):
            output={"Status":"404 this token not found"}
            self.write(output)
        else:
            id_to_response=self.get_argument('id')
            body=self.get_argument('body')
            restoticketmod.db.execute("update ticket set response=%s where id=%s",body,str(id_to_response))
            output={"message":"response to ticket -%d- sent successfully"%id_to_response,"code":"200"}
##########>>>>>>>>>>>>>>>>>def get

class changestatus(BaseHandler):
    db=Database.DATABASE_
    def post(self):
        token_modir=self.get_argument('token')
        if self.check_api(token_modir):
            if not self.check_modir_api(token_modir):
                output={"status":"permiton denied"}
                self.write(output)
        if not self.check_api(token_modir):
            output={"status":"404 this token not found"}
            self.write(output)

        else:
            id_to_response=self.get_argument('id')
            status=self.get_argument('status')
            changestatus.db.execute("update ticket set state=%s where  id=%s",status,str(id_to_response))
            output = {"message": "status ticket with id -%d- changed successfully" % id_to_response, "code": "200"}

            self.write(output)

#######-----------> def get
def main():
        tornado.options.parse_command_line()
        httpserver = tornado.httpserver.HTTPServer(Aplication())
        httpserver.listen(options.port)
        tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
        main()


