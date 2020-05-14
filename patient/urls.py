from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home/',views.mainhome, name='mainhome'),
    path('',views.index, name="p_Home"),
    path('signin/',views.signin, name="p_Signin"),
    path('signup/',views.signup, name="p_Signup"),
    path('plogout/',views.plogout,name='plogout'),
    path('about/',views.about, name="p_about"),
    path('consultation/',views.consultation, name="p_consultation"),
    path('dashboard/',views.dashboard, name="p_Dashboard"),
    path('profile/',views.profile, name="p_patientProfile"),
    path('p_editprofile/',views.p_edit, name='p_edit'),
    path('search_doctor/<int:pk>/',views.search_doctor, name="p_searchdoctor"),
    # path('srch_doctor/<slug:typeofdoc>',views.srch_doctor, name="p_srchdoctor"),
    path('appointment_doc/<int:pk>/',views.appointment_doc, name="appointment_doc"),
    path('treatment/',views.treatment, name="p_Treatment"),
    path('p_appointment/',views.p_appointment, name='p_appointment'),
    path('p_new_chat_req/<int:pk>/',views.new_chat_req, name='p_new_chat_req'),
    path('p_chat_req/',views.chat_req, name='p_chat_req'),
    path('p_chatting/<int:pk>/',views.p_chatting, name='p_chatting'),
    path('p_chat_closed/<int:pk>/', views.p_chat_closed, name='p_chat_closed'),


    path('p_print_consultation/<int:pk>/',views.p_print_consultation,name='p_print_consultation'),

    path('handlerequest/', views.handlerequest, name='HandleRequest'),
    path('makepayment/<int:pk>', views.makepayment, name='makepayment'),

    path('list/',views.PatientListView.as_view(), name='list'),
    path('patient/<int:pk>', views.PatientDetails.as_view(),name='patient_details'),
    path('patientProfile/',views.PatientProfile.as_view(), name='patient_profile'),

    path('post/', views.post, name='post'),
    path('messages/', views.messages, name='messages'),


    path('chattest/<int:pk>/',views.chattest, name='chattest' )


]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)