import torndb
from datetime import date




def main():
	db= torndb.Connection(host='localhost', database='network', user='root', password='s@mba123@li14')
	token="12345"
	subject="sajjad123"	
	body="hellow how are you"
	cdate=str(date.today())
	db.execute("INSERT INTO ticket (token,subject,body,cdate)" "values (%s,%s,%s,%s)",token,subject,body,cdate )	
	user=db.query("select * from ticket where token=%s",token)
	output = {'message': 'ticket sent success fully', 'id':id, 'code': '200'}
	

if __name__=="__main__":
	main()
