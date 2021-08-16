# Django Project Management System

I have built a project management system using Django intended to be used by construction companies who would like to keep track of their clients, projects and tasks in the projects. It can also keep a track of the staff members working for a company and also staff members can be assigned to each individual task. 
The admin will have control over the entire system i.e. they can
- Add, edit, delete clients
- Add, edit, delete staff
- Add, edit, delete projects
- Add, edit, delete tasks
- Add, edit, delete contracts
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

- You can enter the dummy admin credentials to login
- The admin dashboard looks like this
- ![dashboard](https://user-images.githubusercontent.com/64229911/129622818-c0a0dc64-73bd-4084-a61a-f94cc1092b94.PNG)
- You will be able to see the count of existing clients, staff, projects and Tasks on the dashboard.
- There is a settings option through which admin details can be changed.
- The sidebar contains details about Staff, Clients, Projects, Tasks, Contracts, Suppliers, Services, Parts, Payments.
- On clicking on any of the links, existing entries from the database can be viewed and edited. Also, new details can be added for each of these.
- For example the on clicking staff, you will see the following
- ![Staff](https://user-images.githubusercontent.com/64229911/129623230-3f6ded23-4376-4fc8-9cdc-a5e1a5f89f9a.PNG)
- As you can see, each individual entry can be edited and deleted.
- Also, there is a Add Staff button where you can add new staff members. The page looks like this.
- ![add staff](https://user-images.githubusercontent.com/64229911/129623396-3f8ba93f-2298-41c7-9a0c-eb49c1ce8d45.PNG)


The recommended workfow before using this application is

-System workflow
- As this application is built for a construction company to keep a track of their projects, clients etc. There will be projects created and the projects will have fixed tasks. For ex - Building project will have a set number of tasks. Electrical project will have its own set of tasks and these tasks will not change under normal circumstances. 
- The admin user will first create a new contract for a new client.
- Then admin will add that client to the system and link the project to the client.
___________________________________________________________________________________________________________________

Here are all the database tables created
I am using pymysql and jupyter notebooks to exceute SQL queries on the database.

![sql](https://user-images.githubusercontent.com/64229911/129626193-eb84dff9-829d-41f6-99e2-f4135d0cf26e.PNG)

And here is a working SQL Select statement suing PYMYSQL

![select](https://user-images.githubusercontent.com/64229911/129626474-ded77971-70ed-483d-9825-dbbfa0e410da.PNG)



___________________________________________________________________________________________________________________

# Future Functionalities

I want to include future functionalities wherein I will be making login views for both staff and clients.
- Staff and clients will have their own login credential which they can use and both will have their own views.
- For example - When a staff logs in, they will be able to see the tasks which they are assigned to whereas when a client logs in, they will be able to see their open projects.

____________________________________________________________________________________________________________________

I have built this independent project for credits in college. I used AWS cloud9 to do the coding which included Django, HTML, CSS and Javascript to make a beautiful and responsive web application. I have used Amazon RDS instance of MYSQL database.

Learnings

- AWS cloud9
- AWS RDS
- Django 3.1
- MYSQL
- HTML
- CSS
- Javascript
- Basics of AGILE development.

