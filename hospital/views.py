from django.shortcuts import render,redirect,reverse
import numpy as np
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.core.files.base import ContentFile
import pyqrcode
from PIL import Image
import joblib
import pickle
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import os
from sklearn.linear_model import LogisticRegression
#commented_for_jeevan
# from keras.preprocessing import image
#commented_for_jeevan 
# from keras.models import Sequential, load_model
from django.shortcuts import render
#commented_for_jeevan 
# from keras.applications.vgg16 import preprocess_input
#commented_for_jeevan 
# model69 = load_model('chest_xray.h5')
#commented_for_jeevan 
# model = load_model('model111.h5')
from .models import Appointment, Patient
from django.views.static import serve
#commented_for_jeevan
# model222=load_model("newmodel.h5")
logreg=LogisticRegression()

UPLOAD_FOLDER = os.path.join(settings.BASE_DIR, 'uploads')
STATIC_FOLDER = os.path.join(settings.BASE_DIR, 'static')
# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index2.html')

# def generate_qr_codes(strings, prefix='myqr'):
#     for i, s in enumerate(strings):
#         # Generate QR code
#         qr = pyqrcode.create(s)
        
#         # Save the QR code as SVG
#         qr.svg(f'{prefix}_{i+1}.svg', scale=8)
        
#         # Save the QR code as PNG
#         qr.png(f'{prefix}_{i+1}.png', scale=6)


#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')


#for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')

def homeclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index2.html')


#for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html')

def conclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/contact.html')


def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})




def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'hospital/doctorsignup.html',context=mydict)


def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            # patient.assignedDoctorId=request.POST.get('assignedDoctorId')

             # Open the image file and assign it to the qr_code field
            # userId= patient.user.user_id;
            userId = patient.user.pk;
            qr = pyqrcode.create(userId)
            # Save the QR code as SVG
            qr.svg(f'./static/generated_QRs/qrcode.svg', scale=8)
            # Save the QR code as PNG
            qr.png(f'./static/generated_QRs/qrcode.png', scale=6)

            qr_code_path = './static/generated_QRs/qrcode.png'
            with open(qr_code_path, 'rb') as f:
                # Use ContentFile to create a Django File from the image content
                patient.qrCode.save('image.png', ContentFile(f.read()))

            patient.save()
            # patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        else:
            print("UserForm Errors:", userForm.errors)
            print("--------------------------------------------------")
            print("PatientForm Errors:", patientForm.errors)
        return HttpResponseRedirect('patientlogin')
    return render(request,'hospital/patientsignup.html',context=mydict)


# def patient_signup_view(request):
#     if request.method == 'POST':
#         userForm = forms.PatientUserForm(request.POST)
#         patientForm = forms.PatientForm(request.POST, request.FILES)
#         if userForm.is_valid() and patientForm.is_valid():
#             user = userForm.save(commit=False)
#             user.set_password(user.password)
#             user.save()

#             patient = patientForm.save(commit=False)
#             patient.user = user
#             patient.assignedDoctorId = request.POST.get('assignedDoctorId')
#             patient.save()

#             my_patient_group = Group.objects.get_or_create(name='PATIENT')
#             my_patient_group[0].user_set.add(user)

#             return HttpResponseRedirect('patientlogin')

#     else:
#         userForm = forms.PatientUserForm()
#         patientForm = forms.PatientForm()

#     mydict = {'userForm': userForm, 'patientForm': patientForm}
#     return render(request, 'hospital/patientsignup.html', context=mydict)







#-----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'hospital/patient_wait_for_approval.html')








#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'hospital/admin_dashboard2.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/admin_update_patient.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'hospital/admin_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')




#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_discharge_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'hospital/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_add_appointment_view(request):
#     user_id = request.GET.get('user_id', None)
#     print('--admin--add--apointment')
#     print(user_id)
#     appointmentForm=forms.AppointmentForm()
#     mydict={'appointmentForm':appointmentForm,}
#     if request.method=='POST':
#         appointmentForm=forms.AppointmentForm(request.POST)
#         if appointmentForm.is_valid():
#             appointment=appointmentForm.save(commit=False)
#             appointment.doctorId=request.POST.get('doctorId')
#             appointment.patientId=user_id
#             appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
#             appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
#             appointment.status=True
#             appointment.save()
#         return HttpResponseRedirect('admin-view-appointment')
#     return render(request,'hospital/admin_add_appointment.html',context=mydict)
import datetime
from django.db.models import Q
from django.utils import timezone

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    user_id = request.GET.get('user_id', None)
    print('--admin--add--appointment')
    print(user_id)
    appointment = None 
    # try:
    #     appointment = models.Appointment.objects.get(patientId=user_id) 
    #     appointmentForm = forms.AppointmentForm(instance=appointment)
    # except models.Appointment.DoesNotExist:
    #     appointmentForm = forms.AppointmentForm()
    try:
        # Try to get an existing appointment for today and the given patientId
        appointment = models.Appointment.objects.get(
            Q(patientId=user_id) & Q(appointmentDate=timezone.now().date())
        )
        appointmentForm = forms.AppointmentForm(instance=appointment)
        appointment.delete()  
    except models.Appointment.DoesNotExist:
        # If there's no existing appointment, create a new form
        appointmentForm = forms.AppointmentForm()

    mydict = {'appointmentForm': appointmentForm}

    if request.method == 'POST':
        appointmentForm = forms.AppointmentForm(request.POST, instance=appointment)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            print(type(appointment.appointmentDate))
            appointment.appointmentDate = request.POST.get('appointmentDate')
            appointment.appointmentTime = request.POST.get('appointmentTime')
            appointment.patientId = user_id
            appointment.doctorName = models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName = models.User.objects.get(id=user_id).first_name
            appointment.status = True
            appointment.save()
            return HttpResponseRedirect('admin-view-appointment')

    return render(request, 'hospital/admin_add_appointment.html', context=mydict)

# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)

# def appointment_view1111(request):
#     appointment1 = forms.Appointment1()
#     patient_info = None

#     if request.method == 'POST':
#         appointment1 = forms.Appointment1(request.POST)
#         if appointment1.is_valid():
#             patient_id = request.POST.get('patientId')
            
#             try:
#                 patient_info = models.Patient.objects.get(patient_id=patient_id)
#             except models.Patient.DoesNotExist:
#                 patient_info = None

#             if patient_info:
#                 appointment = appointment1.save(commit=False)
#                 appointment.patientId = patient_info.id
#                 appointment.status = True
#                 appointment.save()
#                 return HttpResponseRedirect('appointment')

#     mydict = {'appointmentForm': appointment1, 'patient_info': patient_info}
#     return render(request, 'hospital/appointment.html', context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')


#-------------------------SCANNER --------------------------------------------


# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def view_scanner(request):
#     # context = context_data()

#     return render(request, 'hospital/scanner.html')

def view_scanner(request):
    if request.method == 'POST':
        scanned_content = request.POST.get('scanned_content')
        print('------------------------------------------')
        print(scanned_content)
        return redirect('appointment', patient_id=scanned_content)

    return render(request, 'hospital/scanner.html')

# def admin_add_appointment(request):
#     user_id = request.GET.get('user_id', None)
#     print('--admin--add--apointment')
#     print(user_id)
#     return render(request, 'admin_add_appointment.html', {'patient_id': user_id})

# def view_scanner_main(request):
#     if request.method == 'POST':
#         scanned_content = request.POST.get('scanned_content')
        
#         # Build the URL using reverse with the correct pattern
#         appointment_url = reverse('appointment', kwargs={'patient_id': scanned_content})
        
#         return redirect(appointment_url)

#     return render(request, 'hospital/scanner.html')

# def view_scanner(request):
#     if request.method == 'POST':
#         scanned_content = request.POST.get('scanned_content')
#         appointment1 = forms.Appointment1()
#         try:
#             patient_info = models.Patient.objects.get(user_id=scanned_content)
#         except models.Patient.DoesNotExist:
#             patient_info = None

#         if patient_info:
#             appointment1.patient_id = scanned_content
#             appointment = appointment1.save(commit=False)
#             appointment = appointment1.save(commit=False)
#             appointment.patientId = patient_info.id
#             appointment.status = True
#             appointment.save()
#             mydict = {'appointmentForm': appointment1, 'patient_info': patient_info}
#             # return render(request, 'hospital/appointment.html', context=mydict)
#             return redirect('appointment', patient_id=scanned_content)

#     return render(request, 'hospital/scanner.html')



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def appointment_view(request,patient_id=None):
#     appointment1 = forms.Appointment1()
#     patient_info = None
#     print("Patient ID:", patient_id)
#     if request.method == 'POST':
#         appointment1 = forms.Appointment1(request.POST)
#         if appointment1.is_valid():
#             patient_id = appointment1.cleaned_data.get('patientId')
#             print("Patient ID:", patient_id)
#             try:
#                 patient_info = models.Patient.objects.get(user_id=patient_id)
#             except models.Patient.DoesNotExist:
#                 patient_info = None

#             if patient_info:
#                 appointment = appointment1.save(commit=False)
#                 appointment.patientId = patient_info.id
#                 appointment.status = True
#                 appointment.save()

    
#                 mydict = {'appointmentForm': appointment1, 'patient_info': patient_info}
#                 return render(request, 'hospital/appointment.html', context=mydict)

#     # If no patient info is found or form is not submitted
#     mydict = {'appointmentForm': appointment1, 'patient_info': None}
#     return render(request, 'hospital/appointment.html', context=mydict)


import datetime

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def appointment_view(request,patient_id=None):
    appointment1 = forms.Appointment1()
    patient_info = None
    appointment_info = None
    # appointment_info = models.Appointment.objects.get(patientId=patient_id)
    print("Patient ID:", patient_id)
    if patient_id:
        try:
            patient_info = models.Patient.objects.get(user_id=patient_id)
            appointment_info = models.Appointment.objects.filter(patientId=patient_id).first()
        except models.Patient.DoesNotExist:
            patient_info = None

        if patient_info:
            if not appointment_info:
                appointment1.patient_id = patient_id
                appointment = appointment1.save(commit=False)
                appointment.patientId = patient_id
                appointment.appointmentDate = datetime.datetime.today
                appointment.status = True
                appointment.save()  
    if request.method == 'POST':
        appointment1 = forms.Appointment1(request.POST)
        if appointment1.is_valid():
            patient_id = appointment1.cleaned_data.get('patientId')
            print("Patient ID:", patient_id)
            try:
                patient_info = models.Patient.objects.get(user_id=patient_id)
                appointment_info = models.Appointment.objects.filter(patientId=patient_id).first()
            except models.Patient.DoesNotExist:
                patient_info = None

            if patient_info:
                if not appointment_info:
                    appointment1.patient_id = patient_id
                    appointment = appointment1.save(commit=False)
                    appointment.patientId = patient_id
                    appointment.status = True
                    appointment.save()
                mydict = {'appointmentForm': appointment1, 'patient_info': patient_info}
                return render(request, 'hospital/appointment.html', context=mydict)
    
    mydict = {'appointmentForm': appointment1, 'patient_info': patient_info}
    return render(request, 'hospital/appointment.html', context=mydict)

   

# def appointment_view(request, patient_id=None):
#     appointment_form = forms.Appointment1()
#     patient_info = None
#     appointment_info = None

#     print("Patient ID:", patient_id)

#     if patient_id:
#         try:
#             patient_info = models.Patient.objects.get(user_id=patient_id)
#             appointment_info = models.Appointment.objects.get(patientId=patient_info.id)
#         except (models.Patient.DoesNotExist, models.Appointment.DoesNotExist):
#             patient_info = None
#             appointment_info = None

#         if not appointment_info:
#             # If appointment doesn't exist, create a new one
#             if request.method == 'POST':
#                 appointment_form = forms.Appointment1(request.POST)
#                 if appointment_form.is_valid():
#                     appointment = appointment_form.save(commit=False)
#                     appointment.patientId = patient_info.id
#                     appointment.status = True
#                     appointment.save()

#     mydict = {'appointmentForm': appointment_form, 'patient_info': patient_info, 'appointment_info': appointment_info}
#     return render(request, 'hospital/appointment.html', context=mydict)

# def view_scanner(request):
#     if request.method == 'POST':
#         scanned_content = request.POST.get('scanned_content')
#         return redirect('appointment', patient_id=scanned_content)

#     # Retrieve patient ID from query parameters
#     patient_id = request.GET.get('patient_id', None)

#     return render(request, 'hospital/scanner.html', {'patient_id': patient_id})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard2.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_predictions(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) 
    return render(request,'hospital/doctor_predictions.html',{'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_diabetes(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) 
    return render(request,'hospital/diabetes.html',{'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_kidney(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) 
    return render(request,'hospital/kidney.html',{'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doc_liver(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) 
    return render(request,'hospital/liver.html',{'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def malaria(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) 
    return render(request,'hospital/malaria.html',{'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def pneumonia(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) 
    return render(request,'hospital/pneumonia.html',{'doctor':doctor})

def api(full_path):
    #commented_for_jeevan
    # data = image.load_img(full_path, target_size=(50, 50, 3))
     #Please comment next line
    data = '0101'
    data = np.expand_dims(data, axis=0)
    data = data * 1.0 / 255

    #with graph.as_default():
    #commented_for_jeevan
    predicted = ""
    # predicted = model.predict(data)
    return predicted

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def upload_image(request):
    if request.method == 'GET':
        return render(request, 'malaria.html')
    elif request.method == 'POST':
        try:
            file = request.FILES['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.name)
            print(full_name)
            with open(full_name, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            indices = {0: 'PARASITIC', 1: 'Uninfected', 2: 'Invasive carcinomar', 3: 'Normal'}
            result = api(full_name)
            print(result)

            predicted_class = np.ndarray.item(np.argmax(result, axis=1))
            accuracy = round(result[0][predicted_class] * 100, 2)
            label = indices[predicted_class]
            return render(request,'hospital/predict.html',{'image_file_name':file.name,'label': label,'accuracy': accuracy})
           
        except Exception as e:
          return HttpResponse(f"An error occurred: {str(e)}", status=500)


# def api2(full_path):
#    #commented_for_jeevan
#     data = image.load_img(full_path, target_size=(64, 64, 3))
#     #Please comment next line
#     # data = '0101101'
#     data = np.expand_dims(data, axis=0)
#     data = data * 1.0 / 255

#     #with graph.as_default():
#     #commented_for_jeevan
#     predicted = model222.predict(data)
#      #Please comment next line
#     predicted = ''
#     return predicted

def api3(full_path):
#commented_for_jeevan 
    # data = image.load_img(full_path, target_size=(224,224))
    # data = x=image.img_to_array(data)
    # data = np.expand_dims(data, axis=0)
    # img_data=preprocess_input(data)
    # classes=model69.predict(img_data)
    return "classes"

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def upload_image2(request):
    if request.method == 'GET':
        return render(request, 'pneumonia.html')
    elif request.method == 'POST':
        try:
            file = request.FILES['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.name)
            print(full_name)
            with open(full_name, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # indices = {0: 'Normal', 1: 'Pneumonia'}
            result = api3(full_name)
            ans = result[0][0]
            if ans > 0.5000:
                label = 'Normal'
                accuracy = ans*100.00
            else:
                label = 'Pneumonia'
                accuracy = 100.00 - (ans * 100.00)


            # You might want to save the prediction to your model
            # e.g., YourModel.objects.create(image_path=full_name, label=label, accuracy=accuracy)

            return render(request, 'hospital/predict2.html', {'image_file_name': file.name, 'label': label, 'accuracy': accuracy})

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}",status=500)
                                
# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def upload_image2(request):
#     if request.method == 'GET':
#         return render(request, 'pneumonia.html')
#     elif request.method == 'POST':
#         try:
#             file = request.FILES['image']
#             full_name = os.path.join(UPLOAD_FOLDER, file.name)
#             print(full_name)
#             with open(full_name, 'wb') as destination:
#                 for chunk in file.chunks():
#                     destination.write(chunk)

#             indices = {0: 'Normal', 1: 'Pneumonia'}
#             result = api2(full_name)
#             if(result>50):
#                 label= indices[1]
#                 accuracy= result
#             else:
#                 label= indices[0]
#                 accuracy= 100-result
#             return render(request,'hospital/predict2.html',{'image_file_name':file.name,'label': label,'accuracy': accuracy})
           
#         except Exception as e:
#           return HttpResponse(f"An error occurred: {str(e)}", status=500)

        
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)       
def serve_file(request, filename):

    file_path = os.path.join(settings.UPLOAD_FOLDER, filename)
    
    # Use the serve view function to serve the file
    response = serve(request, filename, document_root=settings.UPLOAD_FOLDER)

    return response

def ValuePredictor(to_predict_list, size):
     to_predict = np.array(to_predict_list).reshape(1, size)
     if size == 8:  # Diabetes
        with open("model1.pkl", "rb") as model_file:
            loaded_model = pickle.load(model_file)
        result = loaded_model.predict(to_predict)
     elif size == 30:  # Cancer
        with open("model.pkl", "rb") as model_file:
            loaded_model = pickle.load(model_file)
        result = loaded_model.predict(to_predict)
     elif size == 12:  # Kidney
        with open("modelkid.pkl", "rb") as model_file:
            loaded_model = pickle.load(model_file)
        result = loaded_model.predict(to_predict)
     elif size == 10: #liver
        with open("modelliv.pkl", "rb") as model_file:
            loaded_model = pickle.load(model_file)
        result = loaded_model.predict(to_predict)
     elif size == 11:  # Heart
        with open("model2.pkl", "rb") as model_file:
            loaded_model = pickle.load(model_file)
        result = loaded_model.predict(to_predict)
     return result[0]

def diabetes_result(request):
    if request.method == 'POST':
        to_predict_list = [request.POST.get('Pregnancies', 0),
                           request.POST.get('Glucose', 0),
                           request.POST.get('BloodPressure', 0),
                           request.POST.get('SkinThickness', 0),
                           request.POST.get('Insulin', 0),
                           request.POST.get('BMI', 0),
                           request.POST.get('DiabetesPedigreeFunction', 0),
                           request.POST.get('Age', 0)]
    
        to_predict_list = list(map(float, to_predict_list))
        
        
        if len(to_predict_list) == 8:  # Diabetes
            result = ValuePredictor(to_predict_list, 8)
       

        if int(result) == 1:
            prediction = 'Sorry ! Suffering'
        else:
            prediction = 'Congrats ! you are Healthy'

        return render(request, 'hospital/diabetes-result.html', {'prediction': prediction})

    return HttpResponse("Invalid request method")

def liver_result(request):
    if request.method == 'POST':
        to_predict_list = [float(request.POST.get('Age', 0)),
                1 if request.POST.get('Gender', '').lower() == 'male' else 0,
                float(request.POST.get('Total_Bilirubin', 0)),
                float(request.POST.get('Direct_Bilirubin', 0)),
                float(request.POST.get('Alkaline_Phosphotase', 0)),
                float(request.POST.get('Alamine_Aminotransferase', 0)),
                float(request.POST.get('Aspartate_Aminotransferase', 0)),
                float(request.POST.get('Total_Protiens', 0)),
                float(request.POST.get('Albumin', 0)),
                float(request.POST.get('Albumin_and_Globulin_Ratio', 0))
                           ]
    
        to_predict_list = list(map(float, to_predict_list))
        

        if len(to_predict_list) == 10:  
            result = ValuePredictor(to_predict_list, 10)
       

        if int(result) == 1:
            prediction = 'Sorry ! Suffering'
        else:
            prediction = 'Congrats ! you are Healthy'

        return render(request, 'hospital/liver-result.html', {'prediction': prediction})

    return HttpResponse("Invalid request method")

def kidney_result(request):
    if request.method == 'POST':
        age =  float(request.POST.get('age', 0))
        bp  =  float(request.POST.get('bp', 0))
        al  =  float(request.POST.get('al', 0))
        pcc =  1 if request.POST.get('pcc', '').lower() == 'present' else 0              
        bgr =  float(request.POST.get('bgr', 0))                 
        bu  =  float(request.POST.get('bu', 0))                 
        sc  =  float(request.POST.get('sc', 0))          
        hemo = float(request.POST.get('hemo', 0))                  
        pcv =  float(request.POST.get('pcv', 0))         
        htn =  1 if request.POST.get('htn', '').lower() == 'yes' else 0                 
        dm  =  1 if request.POST.get('dm', '').lower() == 'yes' else 0                  
        appet = 1 if request.POST.get('appet', '').lower() == 'good' else 0                   
                           
                         
    
        
        to_predict_list = [age, bp, al, pcc, bgr, bu, sc, hemo, pcv, htn, dm, appet ]
        to_predict_list = list(map(float, to_predict_list))

        if len(to_predict_list) == 12:  
            result = ValuePredictor(to_predict_list, 12)
       

        if int(result) == 1:
            prediction = 'Sorry ! Suffering'
        else:
            prediction = 'Congrats ! you are Healthy'

        return render(request, 'hospital/kidney-result.html', {'prediction': prediction})

    return HttpResponse("Invalid request method")

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    # 'doctorName':doctor.get_name,
    # 'doctorMobile':doctor.mobile,
    # 'doctorAddress':doctor.address,
    # 'symptoms':patient.symptoms,
    # 'doctorDepartment':doctor.department,
    # 'admitDate':patient.admitDate,
    }
    return render(request,'hospital/patient_dashboard2.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            if doctor.department == 'Cardiologist':
                if 'heart' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})


            if doctor.department == 'Dermatologists':
                if 'skin' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Emergency Medicine Specialists':
                if 'fever' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Allergists/Immunologists':
                if 'allergy' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Anesthesiologists':
                if 'surgery' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Colon and Rectal Surgeons':
                if 'cancer' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})





            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'hospital/patient_book_appointment.html',context=mydict)





@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_profile(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_profile.html',{'patient':patient})

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def available_doctors(request):
    doctor=models.Doctor.objects.all() #for profile picture of patient in sidebar
    patient=models.Patient.objects.get(user_id=request.user.id) 
    return render(request,'hospital/available_doctors.html',{'doctor':doctor ,'patient':patient })




@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_profile(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_profile2.html',{'doctor':doctor})



#for admin
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def patient_profile_ind(request,patient_id):
    patient=models.Patient.objects.get(user_id=patient_id) #for profile picture of patient in sidebar
    appointments = models.Appointment.objects.filter(patientId=patient_id)
    return render(request,'hospital/admin_patient_profile.html',{'patient':patient,'appointments': appointments})

#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------



#Developed By : sumit kumar
#facebook : fb.com/sumit.luv
#Youtube :youtube.com/lazycoders
