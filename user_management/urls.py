from django.urls import path

from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("login/", login, name="login"),
    path("dashboard_page",dashboard_page,name="dashboard_page"),
    path('get_all_user/',get_all_user,name='get_all_user'),
    path('logout',logout,name='logout'),
    path('edit_info/<int:id>/',edit_info,name='edit_info'),
    path('add_edit',add_edit,name='add_edit'),
    path('delete_info/<int:id>/',delete_info,name='delete_info'),
    path('add_info/',add_info,name='add_info'),
    path('add_patient_info/<int:id>/',add_patient_info,name='add_patient_info'),
    path('edit_patient_info',edit_patient_info,name='edit_patient_info'),
    path('patient_details/<int:id>/',patient_details,name='patient_details'),
    path('upload_report/',upload_report,name='upload_report'),
    path('doctor_page',doctor_page,name='doctor_page'),
    path('add_patient_record',add_patient_record,name='add_patient_record'),
    path('add_patient_data',add_patient_data,name='add_patient_data'),
    path('delete_report/<int:id>/',delete_report,name='delete_report'),
    path('doctor_visit',doctor_visit,name='doctor_visit'),
    path('bill/',bill,name='bill'),
    path('discharge',discharge,name='discharge'),
    path('hr_attendance_list',hr_attendance_list,name='hr_attendance_list'),
    # path('download-pdf/',download_pdf, name='download_pdf'),
]
