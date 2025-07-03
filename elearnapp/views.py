from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
import random
from .models import course_details,student_details
from .forms import *
from django.shortcuts import get_object_or_404
from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
def home(request):
    if 'admin' in request.GET:
        return redirect(admindash)
    if 'student'in request.GET:
        return redirect(signup)
    return render(request,'home.html')
def signup(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    elif 'login' in request.GET:
        return redirect('login')
    else:
        form = StudentForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    credtinals={
            "form": StudentForm()
        }
    if request.method=='POST':
        sname=request.POST.get('username')
        password=request.POST.get('password')
        cred=student_details.objects.filter(s_name=sname,s_password=password).first()
        if cred:
            return redirect('main',cred.id)
        else:
            return render(request,'login.html',{"errormessage":'invalid password or username'})
    elif 'forget_password'in request.GET:
        return redirect('forget_password')
    elif 'back'in request.GET:
        return redirect('signup')   
    return render(request,'login.html',credtinals)
 
def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = student_details.objects.filter(s_email=email).first()
        if user:
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.otp_created = timezone.now()
            user.save()
            send_mail(
    'Your OTP for Password Reset',
    f'Your OTP is {otp}',
    settings.EMAIL_HOST_USER,
    [user.s_email],
    fail_silently=False,
)
            return redirect(verify_otp)
        else:
            return render(request, 'forget_password.html', {'error': 'Email not found'})
    return render(request, 'forget_password.html')

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        entered_otp = request.POST.get('otp')
        print(entered_otp)
        user = student_details.objects.filter(otp=entered_otp).first()
        if user and str(user.otp).strip() == str(entered_otp).strip():
            return redirect(new_password)
        else:
            return render(request, 'verify_otp.html', {
                'error': 'Invalid OTP. Please try again.',
                'email': email
            })
    return render(request,"verify_otp.html")

def new_password(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        email = request.POST['email']
        user = student_details.objects.filter(s_email=email).first()
        print(user.s_email)
        if user:
            user.s_password = new_password  
            print(user.s_password)
            user.save()
            return redirect('login')
        else:
            return render(request, 'new_password.html', {
                'error': 'Email not found. Please check again.',
                'email': email
            })
    return render(request, 'new_password.html')
    
def main(request, sid):
    try:
        student = student_details.objects.get(id=sid)
        cd = student.course.all()

        if 'admin' in request.GET:
            return redirect(admindash)
        if 'completed' in request.GET:
            student.status='completed'
            student.save()
            subject = "🎉 Congratulations on Course Completion!"
            message = f"Dear {student.s_name},\n\nCongratulations on successfully completing your course! We're incredibly proud of your achievement.\n\nBest wishes,\nYour Learning Team"
            recipient_list = [student.s_email]
            send_mail(subject, message, 'anushasreeanu594@gmail.com', recipient_list)
        return render(request, 'main.html', {'c': student, 'cd': cd})
       


    except student_details.DoesNotExist:
        return HttpResponse("Student not found", status=404)
def admindash(request):
    course=course_details.objects.all()
    if 'create' in request.GET:
        return redirect(course_creation)
    if 'update' in request.GET:
       s = request.GET.get('update')
       return redirect(course_update,s)
    if 'delete' in request.GET:
        s = request.GET.get('delete')
        return redirect(course_delete,s)
    if 'dash' in request.GET:
        return redirect(dash)
    return render(request,'admindash.html',{'course':course})
def dash(request):
    data = student_details.objects.values_list('status', flat=True)
    status_counts = Counter(data)
    labels = status_counts.keys() 
    sizes = status_counts.values()
    fig, ax = plt.subplots(facecolor='white')
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    buffer = BytesIO()
    plt.savefig(buffer, format='png', facecolor=fig.get_facecolor()) 
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')
def course_creation(request):
    if request.method == 'POST':
        form = courseform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admindash')
    else:
        form=courseform()
    return render(request,'course_creation.html',{'form':form})
def course_update(request, s):
    course = course_details.objects.get(course_id=s)
    if request.method=="POST":
        course.course_name=request.POST["updated_course_name"]
        course.course_id=request.POST["updated_course_id"]
        course.course_video=request.POST["updated_course_video"]
        course.save()
        return redirect(admindash)
    return render(request, 'course_update.html', {'course': course})
def course_delete(request, s):
     course = course_details.objects.get(course_id=s)
     course.delete()
     return redirect(admindash)






