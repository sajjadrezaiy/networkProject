mysql -u root -p 13787638
create database network

use network

create table network(username varcaher(50),
		     password varchar(50),
		     token varchar(80),
		     id INT NOT NULL PRIMARY KEY AUTO_INCREMENT
	       	     subjectmessage varchar(100)	
		     bodymessgae varchar(1000)
			)

