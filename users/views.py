from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import *
# paginator
from django.core.paginator import Paginator


def home(request):
    return render(request, "users/homepage.html")


def whytherapy(request):
    return render(request, "users/whytherapy.html")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login(request):
    return render(request, 'users/login.html')


@login_required
def dashboard(request):
    if request.user.user_type == '2':
        if request.method == 'POST':
            form1 = UserUpdate(request.POST, request.FILES, instance=request.user)
            if form1.is_valid():
                form1.save()
        else:
            form1 = UserUpdate(instance=request.user)

        therapist = User.objects.get(id=request.user.id)
        return render(request, 'users/therapistDashboardProfile.html', {'therapist': therapist, 'form1': form1})
    else:
        if request.method == 'POST':
            form1 = UserUpdate(request.POST, request.FILES, instance=request.user)
            if form1.is_valid():
                form1.save()
        else:
            form1 = UserUpdate(instance=request.user)
        patient = User.objects.get(id=request.user.id)
        return render(request, 'users/patientDashboardProfile.html', {'patient': patient, 'form1': form1})


@login_required
def therapistDashboardChat(request):
    therapist = User.objects.get(id=request.user.id)
    xx = Question.objects.filter(therapist=request.user.id)
    pending = 0
    solved = 0
    for x in xx:
        if x.answer == "Reply Pending":
            pending += 1
        else:
            solved += 1
    if request.method == "POST":
        ans = request.POST['solution']
        qid = request.POST['qid']
        obj = Question.objects.get(id=qid)
        obj.answer = ans
        obj.save()
    conversation = Question.objects.filter(therapist=request.user.id).order_by('-time_stamp')
    total = solved + pending
    if total != 0:
        ratio = solved / total
    else:
        ratio = 0
    return render(request, 'users/therapistDashboardChat.html',
                  {'conversation': conversation, 'solved': solved, 'pending': pending, 'total': total, 'ratio': ratio,
                   'therapist': therapist})


@login_required
def patientDashboardChat(request):
    users = User.objects.filter(user_type=2)
    current_patient = int(request.user.id)
    conversation = Question.objects.filter(patient_id=current_patient).order_by('-time_stamp')
    if request.method == 'POST':
        therapist = int(request.POST['therapist'])
        ques = request.POST['Issue']
        Question.objects.create(patient_id=current_patient, therapist_id=therapist, question=ques)
    return render(request, 'users/patientDashboardChat.html', {'therapists': users, 'conversation': conversation})


def deleteAccount(request):
    id = User.objects.get(id=request.user.id)
    id.delete()
    return redirect('home')


def guestContactUs(request):
    if request.method == 'POST':
        form = GuestContactUsForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request, 'users/contact.html', {'form': GuestContactUsForm(), 'successmessage': True})
        # html = "<html><body><p> Thankyou for contacting us!</p></body></html>"
        # return HttpResponse('Thankyou for contacting us!')

    form = GuestContactUsForm()
    return render(request, 'users/contact.html', {'form': GuestContactUsForm(), 'successmessage': False})
