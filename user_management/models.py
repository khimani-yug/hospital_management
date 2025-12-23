from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=25,unique=True)

    def __str__(self):
        return self.name
    
class Department(models.Model):
    name = models.CharField(max_length=25,unique=True)

    def __str__(self):
        return self.name
    

class User(AbstractUser) :
    username = models.CharField(max_length=25,unique=True)
    role =  models.ForeignKey(Role,on_delete=models.SET_NULL,related_name='user_role',null=True)
    department =  models.ForeignKey(Department,on_delete=models.SET_NULL,related_name='user_department',null=True)
    charges = models.IntegerField(default = 0,null=True)
  
    def __str__(self):
        return self.username
    
class Ward(models.Model):
    ward_name = models.TextField(unique=True)
    ward_charges = models.IntegerField()
    

    def __str__(self):
        return self.ward_name

class Bed(models.Model):
    bed_no = models.TextField(unique=True)

    def __str__(self):
        return self.bed_no

class PatientsInformation(models.Model):
    patient_name = models.ForeignKey(User,on_delete=models.CASCADE,related_name='patient_name',null=True)
    admit_date = models.DateField()
    ward_number = models.ForeignKey(Ward,on_delete=models.SET_NULL,related_name='word_number',null=True)
    bed_number =  models.ForeignKey(Bed,on_delete=models.SET_NULL,related_name='bed_number',null=True)
    description = models.TextField()
    doctor = models.ManyToManyField(User,blank=True,related_name='doctor')
    discharge = models.BooleanField(default=False)
    discharge_date = models.DateField(null=True)
    download = models.BooleanField(default = False)

    # def __str__(self):
    #     return self.patient_name 
     
def report_upload_path(instance,filename):
    ext = filename.split(".")[-1]
    file_name = f"{instance.patient_id}.{ext}"
    return f'{file_name}'
    
class Report(models.Model):
    patient_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='patient_id',null=True)
    report = models.FileField(upload_to=report_upload_path)

class PatientHealthReport(models.Model):    
    patient_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='patient_report_id',null=True)
    date = models.DateField(auto_now=True)
    bood_presure = models.CharField(max_length=3)
    sugar = models.CharField(max_length=3)
    oxygen = models.CharField(max_length=3)
    doctor=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='doctor_id',null=True)
    description = models.TextField()
    time = models.TimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient_id} {self.date}"
    
class DoctorVisit(models.Model):
    visited_patient_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='visited_patient_id',null=True)
    doctor_visit_id=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='doctor_visit_id',null=True) 
    date = models.DateField(auto_now=True)
    visit = models.BooleanField(default=False)
    time = models.TimeField(auto_now=True)




    
