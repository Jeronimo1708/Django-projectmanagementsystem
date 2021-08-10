from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# # Choices for timeframe

timeframe = (
        ('7','7 days'),
        ('14','14 days'),
        ('21','21 days'),
        ('28','28 days'),
        ('2','2 months'),
        ('3','3 months'),
        ('5','5 months'),
        ('6','6 months'),
        ('9','9 months'),
        ('12','12 months'),
        ('15','15 months'),
        ('18','18 months'),
        ('21','21 months')
    )
    
States = (
    ('AL', 'Alabama'), 
    ('AK', 'Alaska'), 
    ('AS', 'American Samoa'), 
    ('AZ', 'Arizona'), 
    ('AR', 'Arkansas'), 
    ('AA', 'Armed Forces Americas'), 
    ('AE', 'Armed Forces Europe'), 
    ('AP', 'Armed Forces Pacific'), 
    ('CA', 'California'), 
    ('CO', 'Colorado'), 
    ('CT', 'Connecticut'), 
    ('DE', 'Delaware'), 
    ('DC', 'District of Columbia'), 
    ('FL', 'Florida'), 
    ('GA', 'Georgia'), 
    ('GU', 'Guam'), 
    ('HI', 'Hawaii'), 
    ('ID', 'Idaho'), 
    ('IL', 'Illinois'), 
    ('IN', 'Indiana'), 
    ('IA', 'Iowa'), 
    ('KS', 'Kansas'), 
    ('KY', 'Kentucky'), 
    ('LA', 'Louisiana'), 
    ('ME', 'Maine'), 
    ('MD', 'Maryland'), 
    ('MA', 'Massachusetts'), 
    ('MI', 'Michigan'), 
    ('MN', 'Minnesota'), 
    ('MS', 'Mississippi'), 
    ('MO', 'Missouri'), 
    ('MT', 'Montana'), 
    ('NE', 'Nebraska'), 
    ('NV', 'Nevada'), 
    ('NH', 'New Hampshire'), 
    ('NJ', 'New Jersey'), 
    ('NM', 'New Mexico'), 
    ('NY', 'New York'), 
    ('NC', 'North Carolina'), 
    ('ND', 'North Dakota'), 
    ('MP', 'Northern Mariana Islands'), 
    ('OH', 'Ohio'), 
    ('OK', 'Oklahoma'), 
    ('OR', 'Oregon'), 
    ('PA', 'Pennsylvania'), 
    ('PR', 'Puerto Rico'), 
    ('RI', 'Rhode Island'), 
    ('SC', 'South Carolina'), 
    ('SD', 'South Dakota'), 
    ('TN', 'Tennessee'), 
    ('TX', 'Texas'), 
    ('UT', 'Utah'), 
    ('VT', 'Vermont'), 
    ('VI', 'Virgin Islands'), 
    ('VA', 'Virginia'), 
    ('WA', 'Washington'), 
    ('WV', 'West Virginia'), 
    ('WI', 'Wisconsin'), 
    ('WY', 'Wyoming')
    )

# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Staff"), (3, "Client"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
    
    
class AdminUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Contracts(models.Model):
    id = models.AutoField(primary_key=True)
    contract_name = models.CharField(max_length=30, unique=True, default='NA')
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    objects = models.Manager()


class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    
class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=255)
    task_description = models.TextField()
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, default=1) #need to give defauult course
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

	
class Clients(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=30, choices=States)
    project_id = models.ForeignKey(Projects, on_delete=models.DO_NOTHING, default=1)
    contract_id = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
class Payments(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE, default=0.0)
    
class Suppliers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    
class Services(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    supplier_id = models.ForeignKey(Suppliers, on_delete=models.CASCADE)

class Parts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    supplier_id = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    
class Documents(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.FileField()
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    
class Locations(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=30, choices=States)
    
   

    
    
    
    
    
    


