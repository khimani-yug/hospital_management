from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import *
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from weasyprint import HTML  
# pyright: ignore[reportMissingImports]
# from django.contrib.auth.hashers import check_password
# from django.core import management
# import requests
from django.http import JsonResponse

def home(request):
    user_data = request.session.get('user_data',None)
    if user_data:
        if user_data["role"]["name"] == 'Receptionist' :
           return redirect('/get_all_user/')
        elif user_data["role"]["name"] == 'Doctor' :
            return redirect('doctor_page') 
        elif user_data["role"]["name"]  == 'Patient' :
            return redirect(f'patient_details/{user_data["id"]}/')
        return redirect('/admin/')
    else:
        return render(request, 'login.html')



def login(request):   
 
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username,password=password)

    if user is None :
        #Display an eror message if authentication fails (invalid password)
        messages.error(request,"Invalid Usrename or Password")
        return redirect('/')
    else:
        auth_login(request, user)
        user_data = {
                    "id" : user.id,
                    "username":user.username,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "email":user.email,
                    "role":{"name":user.role.name}
                    }
        request.session['user_data'] = user_data

        if user.role.name.lower() == 'admin':
            return redirect('/admin/')
        else:
            return redirect('dashboard_page')
    
def dashboard_page(request):
    roles = Role.objects.all()
    user_data = request.session.get('user_data',None)
    if user_data:
        user_roles = []
        for i in roles :
            user_roles.append({"id":i.id,"name":i.name})

        request.session["user_roles"] = user_roles

        request.session.modified = True
        if user_data["role"]["name"] == 'Receptionist' :
           return redirect('/get_all_user/')
        elif user_data["role"]["name"] == 'Doctor' :
            return redirect('doctor_page') 
        elif user_data["role"]["name"]  == 'Patient' :
            return redirect(f'patient_details/{user_data["id"]}/')
    else:
        return redirect('/')

def get_all_user(request):
    user_role = request.GET.get('user_role',None)
    users = User.objects.all().order_by("id")
    search = request.GET.get('search',"")
    discharge_patient = PatientsInformation.objects.filter(discharge=True).values_list('patient_name', flat=True)
    # discharged_patients = PatientsInformation.objects.filter(discharge=True)


    if user_role not in ["None",None,'']:
        users = User.objects.filter(role=user_role)

        add_user_role = Role.objects.get(id=user_role)
    else :
        add_user_role = None


    if search not in ["None",None,'']:
        users = users.filter(username__icontains = search)

        add_user_role = None

    p = Paginator(users, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    


    data = {"users":users,
            "add_user_role":add_user_role,
            'page_obj': page_obj,
            "user_role":user_role,
            "total_page":p.num_pages,
            "search":search,
            'discharge_patient': discharge_patient,
        
            }
    return render(request, 'dashboard.html',context=data)

def logout(request):
    auth_logout(request)
    del request.session
    return redirect('/')

def edit_info(request,id):
    if id:
      users_info = User.objects.get(id=id)
      roles=Role.objects.all()
      department=Department.objects.all()
      data = {"users_info":users_info,
              "roles":roles,
              "departments":department,
              
              }
      return render(request, 'edit_user.html', context=data)

    
    data = {"user_info":users_info}

    return render(request, 'dashboard.html', context=data)

from hospital_management.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
def send_email(data,password):
    subject = 'Welcome to Radhakrishna Multispecialty Hospital'
    text_content = 'Welcome to Radhakrishna Multispecialty Hospital - Your login credentials are enclosed below.'

    html_content = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Welcome to Radhakrishna Multispecialty Hospital</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <table width="100%" style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <tr>
                <td style="background-color: #00695c; padding: 20px; color: white; border-top-left-radius: 10px; border-top-right-radius: 10px; text-align: center;">
                    <h2 style="margin: 0;">Radhakrishna Multispecialty Hospital</h2>
                    <p style="margin: 0; font-size: 14px;">Committed to Excellence in Healthcare</p>
                </td>
            </tr>
            <tr>
                <td style="padding: 20px;">
                    <p style="font-size: 16px; color: #333;"><strong>Dear {data.first_name}  {data.last_name},</strong></p>
                    <p style="font-size: 15px; color: #333;">Welcome to Radhakrishna Multispecialty Hospital. Your account has been successfully created.</p>
                    
                    <p style="font-size: 15px; color: #333;">Below are your login credentials:</p>
                    <ul style="font-size: 15px; color: #333; padding-left: 20px;">
                        <li><strong>Username:</strong> {data.username}</li>
                        <li><strong>Password:</strong> {password}</li>
                    </ul>

                    <p style="font-size: 14px; color: #666;">Please use the credentials above to log into the hospital portal. You are advised to change your password upon first login for security purposes.</p>
                    
                    <br/>
                    <p style="font-size: 14px; color: #999;">If you need any assistance, feel free to reach out to the hospital help desk.</p>
                    <p style="font-size: 14px; color: #999;">Regards,<br/>Radhakrishna Hospital Team</p>
                </td>
            </tr>
            <tr>
                <td style="background-color: #e0f2f1; padding: 15px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; text-align: center; font-size: 13px; color: #555;">
                    © 2025 Radhakrishna Multispecialty Hospital. All Rights Reserved.
                </td>
            </tr>
        </table>
    </body>
    </html>"""

    from_email = EMAIL_HOST_USER
    to_emails = [data.email]
    email = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
    email.attach_alternative(html_content, 'text/html')
    email.send()

def add_edit(request):
    try:
        id = request.POST.get('id',None)
        username = request.POST.get('edit_name',None)
        email = request.POST.get('edit_email',None)
        fname = request.POST.get('edit_fname',None)
        lname = request.POST.get('edit_lname',None)
        role =  request.POST.get('edit_role',None)
        department =  request.POST.get('edit_department',None)
        charges = request.POST.get('charges',None)
        password = request.POST.get('password',None)
        repassword = request.POST.get('repassword',None)
        if charges == "":
           charges=0


        if id :
            edit_add = User.objects.get(id = id)
            password = edit_add.password
        else:
            if password != repassword:
                messages.error(request,"Both Passwords are diffrent")
                # user_info = dict(request.POST)

                user_info ={
                        "id" : "",
                        "username":username,
                        "first_name":fname,
                        "last_name":lname,
                        "email":email,
                        "role":role,
                        "department":department
                        }
                
                roles=Role.objects.all()
                department=Department.objects.all()
                data = {"users_info":user_info,
                        "roles":roles,
                        "departments":department}
                return render(request,'edit_user.html',context=data)
            edit_add = User()

        role_add = Role.objects.get(id=role)

        department_add = Department.objects.get(id=department)


        edit_add.username = username
        edit_add.email = email
        edit_add.first_name = fname
        edit_add.last_name = lname
        edit_add.role = role_add
        edit_add.department = department_add
        edit_add.charges = charges
        
        if not id :
            hashed_password = make_password(password)
            edit_add.password = hashed_password
        
        edit_add.save()

        send_email(edit_add,password)
        return redirect('/get_all_user')


    except:
        id = request.POST.get('id',None)
        email = request.POST.get('edit_email',None)
        fname = request.POST.get('edit_fname',None)
        lname = request.POST.get('edit_lname',None)
        role =  request.POST.get('edit_role',None)
        department =  request.POST.get('edit_department',None)
        charges = request.POST.get('charges',None)

        messages.error(request,"Username is not unique")

        user_info ={
                        "id" : "",
                        "first_name":fname,
                        "last_name":lname,
                        "email":email,
                        "role":role,
                        "department":department,
                        "charges":charges
                        }
        roles=Role.objects.all()
        department=Department.objects.all()
        data = {"users_info":user_info,
                        "roles":roles,
                        "departments":department}
        return render(request,'edit_user.html',context=data)




def delete_info(request,id):
    d=User.objects.get(id=id)
    d.delete()

    return redirect('/get_all_user')

def add_info(request):
    user_role = request.GET.get('role',None)
    department=Department.objects.all()
    roles=Role.objects.all()
    data = {  "roles":roles,
              "departments":department,
              "user_role":user_role}
    return render(request,'edit_user.html',context=data)

def add_patient_info(request,id):
    users_info = User.objects.get(id=id)
    roles=Role.objects.all()
    department=Department.objects.all()
    doctor = User.objects.filter(role__name = "Doctor")
    ward = Ward.objects.all()
    bed = Bed.objects.all()

    try:
        patients_info = PatientsInformation.objects.get(patient_name= users_info)
    except:
        patients_info = None

    data = {"users_info":users_info,
            "roles":roles,
            "departments":department,
            "doctor":doctor,
            "ward":ward,
            "bed":bed,
            "patient_info":patients_info}
    return render(request, 'add_patient_info.html', context=data)

def edit_patient_info(request):
    
    username = request.POST.get('edit_name',None)
    admit_date = request.POST.get('admit_date',None)
    ward_no = request.POST.get('ward',None)
    bed_no = request.POST.get('bed',None)
    description = request.POST.get('description',None)
    doctor = request.POST.getlist('doctor',None)

    
    patient_user = User.objects.get(username = username)
    assign_doctor = User.objects.filter(id__in = doctor)
    ward_number = Ward.objects.get(id = ward_no)
    bad_number = Bed.objects.get(id = bed_no)

    if request.POST.get('id',None) :
        patient_add = PatientsInformation.objects.get(patient_name= patient_user)
    else:
        patient_add = PatientsInformation()

    patient_add.patient_name=patient_user

    patient_add.admit_date = admit_date
    patient_add.ward_number = ward_number
    patient_add.bed_number = bad_number
    patient_add.description = description
    patient_add.admit_date = admit_date
    patient_add.save()
    patient_add.doctor.set(assign_doctor)

    return redirect('/')

def patient_details(request,id):
    try :
        patient_detail  = PatientsInformation.objects.get(patient_name__id = id)
    except :
        messages.error(request,"First add patient info")
        patient_id = Role.objects.get(name = 'Patient')
        return redirect(f'/get_all_user/?user_role={patient_id.id}')
        # return redirect(f"url 'get_all_user'?user_role={patient_id.id}")
        
    report = Report.objects.filter(patient_id = id)
    patient_record  = PatientHealthReport.objects.filter(patient_id = id)
    date = datetime.today()
    visited = DoctorVisit.objects.filter(visited_patient_id = id,date = date )
    p = Paginator(patient_record, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    report_page = Paginator(report, 3)
    page_number = request.GET.get('page')
    try:
        page_obj_report = report_page.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj_report = report_page.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj_report = report_page.page(report_page.num_pages)

    

    data = {
        "patient_detail" : patient_detail,
        "report" : report,
        "patient_record" : patient_record,
        "visited" : visited,
        'page_obj': page_obj,
        'page_obj_report': page_obj_report,
        'total_report_page':report_page.num_pages,
        "total_page":p.num_pages,
    }

    return render(request, 'patient_details.html', context=data)

def upload_report(request):
    patient_id = request.POST.get('id',None)
    report = request.FILES.get('file', None)
    enter_report=Report()
    patient_info = User.objects.get(id = patient_id)

    enter_report.patient_id = patient_info
    enter_report.report = report
    if report == None :
        pass
    else :
        enter_report.save()

    return redirect(reverse(f'patient_details',args=[patient_id]))

def doctor_page(request):
    user_data = request.session.get('user_data', None)
    doctor = User.objects.get(id=user_data['id'])
   
    all_wards = Ward.objects.all()  
    ward_id = request.GET.get("ward_id", None)


    if ward_id:
        patient_info = PatientsInformation.objects.filter(doctor=doctor, ward_number=ward_id,discharge=False)
    else:
        patient_info = PatientsInformation.objects.filter(doctor=doctor,discharge=False)

    search = request.GET.get('search',"")

    if search not in ["None",None,'']:
        patient_info = patient_info.filter(patient_name__username__icontains = search)

    p = Paginator(patient_info, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    

    

    patients = User.objects.filter(id__in = patient_info.values_list('patient_name', flat=True))
    date = datetime.today()
    visited = DoctorVisit.objects.filter(visited_patient_id__in = patients,date = date,doctor_visit_id =  doctor).count()
    total = len(patient_info)  * 2

    pending = total - visited 
    data = {
        "patient_info": patient_info,
        "ward_id": int(ward_id) if ward_id else None,
        "all_wards": all_wards,
        "total":total,
        "pending":pending,
        "visited":visited,
        'page_obj': page_obj,
        "total_page":p.num_pages,
        "search":search
    }

    return render(request, 'doctor_dashboard.html', context=data)

def add_patient_record(request):
    patient_detail = request.GET.get('patient_detail',None)
    doctor = request.GET.get('doctor',None)

    patient_id = User.objects.get(id = patient_detail)
    doctor_id = User.objects.get(id = doctor)

    data = {
        "patient_id" : patient_id,
        "doctor_id" : doctor_id
    }

    return render(request, 'add_patient_record.html', context=data)

def add_patient_data(request):
    username_d = request.POST.get('doctor_name',None)
    username_p = request.POST.get('patient_name',None) 
    bp = request.POST.get('bood_presure',None)
    sugar = request.POST.get('sugar',None)
    oxygen = request.POST.get('oxygen',None)
    description = request.POST.get('description',None)
    
    patient_id = User.objects.get(username = username_p)
    doctor_id = User.objects.get(username = username_d)

    helth_report=PatientHealthReport()

    helth_report.patient_id = patient_id
    helth_report.doctor = doctor_id
    helth_report.sugar = sugar
    helth_report.bood_presure = bp
    helth_report.oxygen = oxygen
    helth_report.description = description

    helth_report.save()
    return redirect(f'patient_details/{patient_id.id}/')

def delete_report(request,id):
    
    d=PatientHealthReport.objects.get(id = id)
    patient_id=d.patient_id.id
    d.delete()

    return redirect(reverse(f'patient_details',args=[patient_id]))

def doctor_visit(request):
    patient_id = request.POST.get('visited_patient_id',None)
    doctor_id = request.POST.get('visited_doctor_id',None)
    visiting = request.POST.get('visited',None)

    patient_visit = User.objects.get(id = patient_id)
    doctor_visit = User.objects.get(id = doctor_id)

    visit=DoctorVisit()
    visit.visited_patient_id=patient_visit
    visit.doctor_visit_id=doctor_visit
    visit.visit=bool(visiting)
    visit.save()
    return redirect(f'patient_details/{patient_visit.id}/')

def discharge(request):
    patient_detail = request.GET.get('patient_detail',None)
    patient_info = PatientsInformation.objects.get(patient_name = patient_detail)
    date = datetime.today()
    patient_info.discharge = True
    patient_info.discharge_date = date
    patient_info.save()
    return redirect(f'patient_details/{patient_info.patient_name.id}/')


# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     response = HttpResponse(content_type='application/pdf')
#     pisa_status = pisa.CreatePDF(html, dest=response)
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response
    

def bill(request):
        patient_detail = request.GET.get('patient_detail',None)
        download = request.GET.get('download',None)
    # try:
        patient_info = PatientsInformation.objects.get(patient_name__id = patient_detail)
        doctors = patient_info.doctor.all()
        visiting_charge = dict()
        visiting = list()
        all_doctor_charge = 0
        for doctor in doctors :
            visited = DoctorVisit.objects.filter(visited_patient_id = patient_detail,doctor_visit_id =  doctor.id , visit = True).count()
            if doctor.charges is None:
                total_doctor_charge = 0
            else:
                total_doctor_charge = doctor.charges * visited
            all_doctor_charge = all_doctor_charge + total_doctor_charge
            visiting_charge["name"] = doctor.username
            visiting_charge["visit_charge"] = doctor.charges if doctor.charges is not None else 0
            visiting_charge["Total_visit"] = visited
            visiting_charge["Total_charge"] = total_doctor_charge
            visiting.append(visiting_charge)
        
        if patient_info.discharge_date is None or patient_info.admit_date is None:
            messages.error(request, "Admit Date or Discharge Date is missing")
            return redirect(reverse(f'patient_details', args=[patient_detail]))
        days = (patient_info.discharge_date - patient_info.admit_date).days
        if days < 1:
            days = 1
        if patient_info.ward_number is None:
            messages.error(request, "Ward number is missing")
            return redirect(reverse(f'patient_details', args=[patient_detail]))
        if patient_info.ward_number.ward_charges is None:
            messages.error(request, "Ward charges are missing")
            return redirect(reverse(f'patient_details', args=[patient_detail]))
        if days is None:
            messages.error(request, "Invalid number of days")
            return redirect(reverse(f'patient_details', args=[patient_detail]))
        wardcharge = patient_info.ward_number.ward_charges
        total = days * wardcharge
        final = total + all_doctor_charge
    # except:
    #     messages.error(request,"Admit Date is wrong")
    #     return redirect(reverse(f'patient_details',args=[patient_detail]))
    # else:

        data = {
            "doctor_charge" : visiting,
            "total_ward_charge" : total,
            "total_days" : days,
            "wardcharge" : wardcharge,
            "patient_detail" : patient_info,
            "total_doctor_charge" : all_doctor_charge,
            "total" : final
        } 
        if download :
            # return render_to_pdf('download_bill.html', context_dict=data)
            html_string = render_to_string('download_bill.html', data)
            pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'filename="report.pdf"'
            return response 
        else :
            return render(request, 'bill.html', context=data)
    
# def download_pdf(request):
#     context = {
#         'name': 'Romit',
#         'items': ['Kurti', 'Gown', 'Top']
#     }
#     return render_to_pdf('bill.html', context)

def hr_attendance_list(request):
    try:
        response = request.get("http://192.168.29.16:8000/hr_attendance_list?year=2025&month=4&day=15")
        data = response.json()
        return JsonResponse({'patients': data})
    except request.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)