from django.db import models

def get_default_service():
    return []
def get_default_servic():
    return "abc123@"
class Cdetail(models.Model):
    unique=models.AutoField(primary_key=True)
    profile_image = models.CharField(max_length=5000)
    name=models.CharField(max_length=50)
    phone=models.IntegerField()
    mail=models.CharField(max_length=50)
    gender=models.CharField(max_length=10)
    passw=models.CharField(max_length=30)
    address=models.CharField(max_length=100)
    service = models.JSONField(default=list, null=True, blank=True)
    servicehistory = models.JSONField(   default=get_default_service,null=True, blank=True)

class Ticket(models.Model):
    unique=models.AutoField(primary_key=True)
    mail=models.CharField(max_length=70)
    phone=models.IntegerField()
    ticketdetail=models.TextField(max_length=1500)

class Employee(models.Model):
    unique = models.AutoField(primary_key=True)
    profile_image = models.CharField(max_length=3000)
    name = models.CharField(max_length=70)
    phone = models.IntegerField()
    email = models.CharField(max_length=100)
    passw=models.CharField(max_length=30,default=get_default_servic)
    gender = models.CharField(max_length=10)
    address = models.TextField(max_length=600)
    service_provided = models.CharField(max_length=500)
    experience = models.PositiveIntegerField()
    specialization = models.CharField(max_length=1000)
    description = models.TextField(max_length=2000)
    no_of_service_provided=models.IntegerField()

class Bookings(models.Model):
    unique = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    uniqueuser=models.IntegerField()
    uniqueservice=models.IntegerField()
    advance = models.BooleanField(default=False)
