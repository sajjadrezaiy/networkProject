import torndb

def main():
	db= torndb.Connection(host='localhost', database='network', user='root', password='s@mba123@li14')
	
	token='123'
	user=db.query("select * from ticket where token=%s",token)
	print(user)
    	mainid=user[len(user)-1]['id']
 	id=len(user)
    	subject=user[id-1]['subject']
    	body=user[id-1]['body']
    	status=user[id-1]['state']
    	cdate=user[id-1]['cdate']
	output={'ticket':'tere are -%d-ticket' %id,'code':'200','block %d' %(id-1):{"subject":'%s' %(subject),"body":'%s' %body,"status":'%s' %status,"id":'%d' %id,"date":'%s' %cdate}}
	
	

if __name__=="__main__":
	main()
