from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
import pytz

departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]
work_departments=[('Labour','Labour'),
('Self-employed','Self-employed'),
('Service','Service'),
('Corporate','Corporate'),
('Government/Public Sector','Government/Public Sector'),
('Nonprofit/Volunteer Work','Nonprofit/Volunteer Work'),
]
Blood_group_choices = (
        ('O+' , 'O positive'),
        ('O-' , 'O negative'),
        ('A+' , 'A positive'),
        ('A-' , 'A negative'),
        ('B+' , 'B positive'),
        ('B-' , 'B negative'),
        ('AB+' , 'AB positive'),
        ('AB-' , 'AB negative'),
        )
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Blood_group_choices= models.CharField(max_length=50,choices=Blood_group_choices,default='O+')
    patient_id =   models.CharField(max_length=12)
    gender = models.CharField(max_length=50, choices=(("Male","Male"), ("Female","Female")), default="Male")
    work_department= models.CharField(max_length=50,choices=work_departments,default='Corporate')
    height =  models.CharField(max_length=3, null=True)
    weight =  models.CharField(max_length=3, null=True)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    qrCode= models.ImageField(upload_to='generated_QRs/',null=True,blank=True,default='default.png')
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    mobile2 = models.CharField(max_length=20,null=False)
    history = models.CharField(max_length=100,null=False)
    # assignedDoctorId = models.PositiveIntegerField(null=True,default =0)
    # assignedDoctorId = models.PositiveIntegerField(null=True,default=14)
    dob=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.history+")"


class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    # appointmentDate=models.DateField(auto_now=True)
    appointmentDate=models.DateField(default=datetime.datetime.today)
    
    appointmentTime = models.TimeField(default=timezone.now().time())
    # appointmentTime = models.TimeField(default=timezone.now().astimezone(pytz.timezone('Asia/Kolkata')).time())
    # (auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)

