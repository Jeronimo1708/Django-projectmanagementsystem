Django Project Management System

I have built a project management system using Django intended to be used by construction companies who would like to keep track of their clients, projects and tasks in the projects. It can also keep a track of the staff members working for a company and also staff members can be assigned to each individual task. 
The admin will have control over the entire system i.e. they can
- Add, edit, delete clients
- Add, edit, delete staff
- Add, edit, delete projects
- Add, edit, delete tasks
- Add, edit, delete suppliers
- Add, edit, delete services that the suppliers provide
- Add, edit, delete parts that the suppliers provide
- Add new payments for the clients. Edit and delete them too. 

The admin superuser can be created from the AWS console using Django command > python manage.py createsuperuser
The username and the password for the admin is set at this stage. The admin can then login using their username and password.
I have created a dummy account for the admin
username - admin@admin.com
password - adminadmin

To replicate this project
- Create a new virtual environment on you computer or use a AWS cloud9 container
- Install Django 3.1 using the pip enviornment
- Clone this repository using git clone
- Change the settings.py file as per your configurations
- You can then start the server by the following command > python manage.py runserver (Note: If using AWS you will have to add 8080 at the end of this line)
- If everything is installed successfully, you will be redirected to the login page.
![login](https://user-images.githubusercontent.com/64229911/129592121-da7b2174-98fd-4d4d-adc1-48b5a376882a.PNG)




I want to include future functionalities wherein I will be making login views for both staff and clients.

Workflow

For a new client - first create the contract.
Once contract is created add the client.
Project can be tracked in the projects tab.
There are specific tasks for each project. Every task is assigned to a staff member.

There are Suppliers who provide services are parts for the contruction work which can be stored in this application.
There are payment which correspond to the clients.
____________________________________________________________________________________________________________________

I have built this independent project for credits in college. I used AWS cloud9 to do all the coding which included Django, HTML, CSS and Javascript to make a beautiful and responsive web application. I have use Amazon RDS instance of MYSQL database.

Learnings

AWS cloud9
AWS RDS
Django
MYSQL
HTML
CSS
Javascript
BAsics of AGILE.

