# Create your views here.
from django.shortcuts import render, redirect
from requests import request
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, JsonResponse
from . models import Doctor, ConsultDetails, Consultation
from patient.models import Patient, Appointment, Chatdb, Chat
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request,'doctor/d_index.html')

def about(request):
    return render(request,'doctor/d_about.html')

def consultation(request):
    return render(request,'patient/p_chatting.html')

def treatment(request):
    return render(request,'doctor/d_treatment.html')

def notification(request):
    return render(request,'doctor/d_notification.html')

def chart(request):
    return render(request, 'doctor/chart.html')


# ============================================================================
# DASHBOARD PART
# ============================================================================

@login_required
def dashboard(request):

    appobjs=Appointment.objects.all()
    chatobjs= Chatdb.objects.all()

    total_pat_count = 0
    total_income = 0.0

    app_total_count = 0
    app_accept_count = 0
    app_reject_count = 0

    chat_total_count = 0
    chat_accept_count = 0
    chat_reject_count = 0

    
    income_pending = 0

    for appobj in appobjs:
        if appobj.doc_id == request.user.pk:
            app_total_count +=1
            if appobj.appointment_status == True and appobj.payment_status == True:
                app_accept_count += 1 
                dobj=Doctor.objects.get(pk=appobj.doc_id)
                total_income += dobj.fees
                
            if appobj.reject_status == True:
                app_reject_count += 1

            if (appobj.appointment_status == True and appobj.payment_status == False ):
                dobj=Doctor.objects.get(pk=appobj.doc_id)
                income_pending += dobj.fees


    
    for chatobj in chatobjs:
        if chatobj.doc_id == request.user.pk:
            chat_total_count += 1
            if chatobj.chat_status==True:
                chat_accept_count += 1
            if chatobj.reject_status == True:
                chat_reject_count += 1  

    total_pat_count=app_total_count+chat_total_count

    arg={'total_pat_count':total_pat_count, 'total_income':total_income,'app_total_count':app_total_count, 'app_accept_count':app_accept_count, 'app_reject_count':app_reject_count, 'chat_total_count':chat_total_count, 'chat_accept_count':chat_accept_count,'chat_reject_count':chat_reject_count, 'income_pending':income_pending }
    

    return render(request,'doctor/d_dashboard.html',arg)

# ============================================================================
# SIGNIN SIGNOUT
# ============================================================================

def logout(request):
    auth.logout(request)
    return render(request,'doctor/d_index.html')


def signin(request):
    if request.method == 'POST':

        username =  request.POST.get('username')
        password =  request.POST.get('password')

        user = auth.authenticate(username=username,password=password)



        if user is not None :
            try:
                if (user.doctor.Is_doctor == True ) :
                    auth.login(request,user)

                    request.session['doctorusername'] = user.username

                    return redirect(index)
                else:
                    return HttpResponse ("else part")

            except :
                # messages.info(request,'Invalid USERNAME or PASSWORD')
                return redirect(signin)


        else :
            # messages.info(request,'Invalid ID or PASSWORD')
            return redirect(signin)


    else :
        return render(request,'doctor/d_signin.html')



def signup(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        pin = request.POST.get('pin')
        address = request.POST.get('address')
        mobile_no = request.POST.get('mobile')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        specialist = request.POST.get('specialist')
        qualification = request.POST.get('qualification')
        language = request.POST.get('language')
        fees = request.POST.get('fees')
        time = request.POST.get('time')
        experience = request.POST.get('experience')
        image = request.FILES['image']
        password = request.POST.get('password')
        password1 = request.POST.get('confpassword')


        if password == password1:
            if User.objects.filter(username=username).exists():
                # messages.info(request, 'User name already exists')
                # return redirect('registration')
                return HttpResponse('id exists')

            elif User.objects.filter(email=email).exists():
                # messages.info(request, 'email already exists')
                # return redirect('registration')
                return HttpResponse('email exists')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()

                doctortnew = Doctor(user=user, name=name, dob=dob, pin = pin, address=address,specialist = specialist,  mobile_no=mobile_no, gender=gender,qualification=qualification,language=language ,experience=experience, image= image )
                doctortnew.save()
                condetnew = Consultation(user=user, fees=fees, time=time)
                condetnew.save()
                # messages.info(request, 'User Created Successfully')
                # return HttpResponse('data inputed successfully')
                return redirect(signin)

        # return redirect('login')

    else:
        return render(request,'doctor/d_signup.html')

# =====================================================================================
# PROFILE
# =====================================================================================

@login_required
def profile(request):
    return render(request,'doctor/d_profile.html')


@login_required
def d_profile_edit(request):
    if request.method == 'POST' :
        if request.FILES['image'] is not None:
            user=request.user
            name=request.POST.get('name')
            mobile_no = request.POST.get('mobile')
            address = request.POST.get('address')
            pin = request.POST.get('pin')
            image = request.FILES['image']

            user.doctor.name=name
            user.doctor.mobile_no=mobile_no
            user.doctor.address=address
            user.doctor.pin=pin
            user.doctor.image=image
            user.doctor.save()
            return render(request,'doctor/d_profile.html')
        else:
            user=request.user
            name=request.POST.get('name')
            mobile_no = request.POST.get('mobile')
            address = request.POST.get('address')
            pin = request.POST.get('pin')

            user.doctor.name=name
            user.doctor.mobile_no=mobile_no
            user.doctor.address=address
            user.doctor.pin=pin
            user.doctor.save()
            return render(request,'doctor/d_profile.html')


    else :
        return render(request,'doctor/d_profile_edit.html')




@login_required
def d_consult_details_edit(request):
    if request.method == 'POST':
        user=request.user
        fees=request.POST.get('fees')
        time = request.POST.get('time')



        user.consultation.fees=fees
        user.consultation.time=time
        user.consultation.save()
        return render(request,'doctor/d_profile.html')

    else :
        return render(request,'doctor/d_consult_details.html')



# =========================================================================
# APPOINTMENT PART
# =========================================================================


@login_required
def d_appointment(request):
    objs=Appointment.objects.all()
    patobjs=Patient.objects.all()
    arg={'objs':objs, 'patobjs':patobjs}
    return render(request, 'doctor/d_appointment.html',arg)



@login_required
def d_app_accept(request,pk):
    objs=Appointment.objects.all()
    patobjs=Patient.objects.all()

    appointmentnew = Appointment.objects.get(pk=pk)
    appointmentnew.appointment_status = True
    appointmentnew.save()

    return redirect(d_appointment)


@login_required
def d_app_reject(request,pk):
    objs=Appointment.objects.all()
    patobjs=Patient.objects.all()

    appointmentnew = Appointment.objects.get(pk=pk)
    appointmentnew.reject_status = True
    appointmentnew.save()
    return redirect(d_appointment)


# =========================================================================
# CHATTING PART
# =========================================================================

@login_required
def d_chat(request):
    objs=Chatdb.objects.all()
    patobjs=Patient.objects.all()
    arg={'objs':objs, 'patobjs':patobjs}
    return render(request, 'doctor/d_chat_request.html',arg)


@login_required
def d_chat_accept(request,pk):
    objs=Chatdb.objects.all()
    patobjs=Patient.objects.all()

    chatnew = Chatdb.objects.get(pk=pk)
    chatnew.chat_status = True
    chatnew.closed = False
    chatnew.save()

    return redirect(d_chat)


@login_required
def d_chat_reject(request,pk):
    objs=Chatdb.objects.all()
    patobjs=Patient.objects.all()

    chatnew = Chatdb.objects.get(pk=pk)
    chatnew.reject_status = True
    chatnew.save()
    return redirect(d_chat)


def d_chat_closed(request,pk):
    chatobj = Chatdb.objects.get(pk=pk)
    chatobj.closed = True
    chatobj.save()

    return redirect(index)


@login_required
def d_chatting(request,pk):
    patobj= Patient.objects.get(pk=pk)
    chatobjs = Chatdb.objects.all()
    arg={'patobj':patobj,'chatobjs':chatobjs }
    return render(request, 'doctor/d_chatting.html',arg)



def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        patid = request.POST.get('patid')
        print(patid ,':', msg)

        c = Chat(sender=request.user.pk, message=msg)

        # msg = c.user.username+": "+msg

        if msg != '':
            c.save()
            print("msg saved" + msg)
            return JsonResponse({'msg': msg})
    else:
        return HttpResponse('Request must be POST.')


def messages(request):
    
    if request.method == "GET":

        c = Chat.objects.all()
        # patobj = Patient.objects.get(pk=pk)
        arg={'chat': c}

        return render(request, 'doctor/d_chatbody.html',arg )
