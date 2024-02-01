from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
import pytz

time_slots = [
    ('00:00 - 00:30', '00:00 - 00:30'),
    ('00:30 - 01:00', '00:30 - 01:00'),
    ('01:00 - 01:30', '01:00 - 01:30'),
    ('01:30 - 02:00', '01:30 - 02:00'),
    ('02:00 - 02:30', '02:00 - 02:30'),
    ('02:30 - 03:00', '02:30 - 03:00'),
    ('03:00 - 03:30', '03:00 - 03:30'),
    ('03:30 - 04:00', '03:30 - 04:00'),
    ('04:00 - 04:30', '04:00 - 04:30'),
    ('04:30 - 05:00', '04:30 - 05:00'),
    ('05:00 - 05:30', '05:00 - 05:30'),
    ('05:30 - 06:00', '05:30 - 06:00'),
    ('06:00 - 06:30', '06:00 - 06:30'),
    ('06:30 - 07:00', '06:30 - 07:00'),
    ('07:00 - 07:30', '07:00 - 07:30'),
    ('07:30 - 08:00', '07:30 - 08:00'),
    ('08:00 - 08:30', '08:00 - 08:30'),
    ('08:30 - 09:00', '08:30 - 09:00'),
    ('09:00 - 09:30', '09:00 - 09:30'),
    ('09:30 - 10:00', '09:30 - 10:00'),
    ('10:00 - 10:30', '10:00 - 10:30'),
    ('10:30 - 11:00', '10:30 - 11:00'),
    ('11:00 - 11:30', '11:00 - 11:30'),
    ('11:30 - 12:00', '11:30 - 12:00'),
    ('12:00 - 12:30', '12:00 - 12:30'),
    ('12:30 - 13:00', '12:30 - 13:00'),
    ('13:00 - 13:30', '13:00 - 13:30'),
    ('13:30 - 14:00', '13:30 - 14:00'),
    ('14:00 - 14:30', '14:00 - 14:30'),
    ('14:30 - 15:00', '14:30 - 15:00'),
    ('15:00 - 15:30', '15:00 - 15:30'),
    ('15:30 - 16:00', '15:30 - 16:00'),
    ('16:00 - 16:30', '16:00 - 16:30'),
    ('16:30 - 17:00', '16:30 - 17:00'),
    ('17:00 - 17:30', '17:00 - 17:30'),
    ('17:30 - 18:00', '17:30 - 18:00'),
    ('18:00 - 18:30', '18:00 - 18:30'),
    ('18:30 - 19:00', '18:30 - 19:00'),
    ('19:00 - 19:30', '19:00 - 19:30'),
    ('19:30 - 20:00', '19:30 - 20:00'),
    ('20:00 - 20:30', '20:00 - 20:30'),
    ('20:30 - 21:00', '20:30 - 21:00'),
    ('21:00 - 21:30', '21:00 - 21:30'),
    ('21:30 - 22:00', '21:30 - 22:00'),
    ('22:00 - 22:30', '22:00 - 22:30'),
    ('22:30 - 23:00', '22:30 - 23:00'),
    ('23:00 - 23:30', '23:00 - 23:30'),
    ('23:30 - 00:00', '23:30 - 00:00'),
]


time_slots_1hr = [
    ('00:00 - 01:00', '00:00 - 01:00'),
    ('01:00 - 02:00', '01:00 - 02:00'),
    ('02:00 - 03:00', '02:00 - 03:00'),
    ('03:00 - 04:00', '03:00 - 04:00'),
    ('04:00 - 05:00', '04:00 - 05:00'),
    ('05:00 - 06:00', '05:00 - 06:00'),
    ('06:00 - 07:00', '06:00 - 07:00'),
    ('07:00 - 08:00', '07:00 - 08:00'),
    ('08:00 - 09:00', '08:00 - 09:00'),
    ('09:00 - 10:00', '09:00 - 10:00'),
    ('10:00 - 11:00', '10:00 - 11:00'),
    ('11:00 - 12:00', '11:00 - 12:00'),
    ('12:00 - 13:00', '12:00 - 13:00'),
    ('13:00 - 14:00', '13:00 - 14:00'),
    ('14:00 - 15:00', '14:00 - 15:00'),
    ('15:00 - 16:00', '15:00 - 16:00'),
    ('16:00 - 17:00', '16:00 - 17:00'),
    ('17:00 - 18:00', '17:00 - 18:00'),
    ('18:00 - 19:00', '18:00 - 19:00'),
    ('19:00 - 20:00', '19:00 - 20:00'),
    ('20:00 - 21:00', '20:00 - 21:00'),
    ('21:00 - 22:00', '21:00 - 22:00'),
    ('22:00 - 23:00', '22:00 - 23:00'),
    ('23:00 - 00:00', '23:00 - 00:00'),
]


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
    assignedDoctorId = models.PositiveIntegerField(null=True,default =0)
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
    appointmentDate=models.DateField(default=timezone.now().date())
    
    appointmentTime = models.CharField(max_length=50,choices=time_slots_1hr,default='02:00 - 03:00')
    # appointmentTime = models.TimeField(default=timezone.now().time())
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

