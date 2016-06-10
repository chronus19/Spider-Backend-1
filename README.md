# Spider-Backend-1
Spider Web Dev Inductions - Backend Task 1 (Student's Database)

** View this file in raw mode for better indentation and clarity. 

GENERAL OVERVIEW

#####
 SPIDER BACKEND TASK 1 
 This README.md file will be updated properly, once the project has been completed. 
 These are just for testing the individual parts of the task. 
#####

 This is the first task for Spider WebDev Inductions (Backend). It is basically a Student Database Management System, that allows a user to add, view and edit the information about the students.   
 ( *NOTE :- Spare me for the design, positioning and colours of the site :p ... )

 ------------------------------------------------------------------------------------------------------

 MODULES USED AND BUILD INSTRUCTIONS :-  
Python Version used = 2.7.10

Django version used = 1.9.4
Get it by using the command :-
pip install django

Database used = MySQL 5.7.12
Get it on Windows :-
pip install mysqlclient  
pip install MySQL-python  

Get it on Linux :-  
sudo apt-get install libmysqlclient-dev  
sudo pip install MySQL-python  
  
External Modules Used :-  
1) validate_email   ->  ( Used for validating e-mail address )  
Get it by running the command :-  
pip install validate_email  
  
Database Name :- Spider  
Table Name :- student_student  


If you have the above requisites, you may follow the given steps :-  
1) Clone the repository on a local folder.  
2) For setting up your database connections, open 'mysite\settings.py'. In the 'DATABASES' section, 
   set the NAME as your database name (make sure that it already exists), set the USER and PASSWORD as you username and
   password for setting up the connection with the database, and similarly set the HOST and PORT for the MySQL server.   
     The default values are :- 
	      'NAME': 'spider',  
        'USER' : 'root',  
        'PASSWORD' : 'password',  
        'HOST' : 'localhost',  
        'PORT':'3306',  
3) In your local directory, run the command :-  
		python manage.py makemigrations  
4) In the same directory, run another command :-  
		python manage.py migrate  
5) If the above commands are successful, then you are ready to run your server.  
   Run the command :-  
		python manage.py runserver  
   (OR)   
   Run the script runserver.bat (if you are on Windows)  
     
If this executes without errors, then your server is up and running on port 8000. You can view it by opening 'localhost:8000' in your browser. 
