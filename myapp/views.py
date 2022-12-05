from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def coursedetails(request):
    return render(request,'course-details.html')
def courses(request):
    return render(request,'courses.html')
def events(request):
    return render(request,'events.html')
def pricing(request):
    return render(request,'pricing.html')
def trainers(request):
    return render(request,'trainers.html')
def registration(request):
    if request.method == 'GET':
        return render(request,'registration.html')
    else:
        print(request.POST['Name'],
        request.POST['Email'],
        request.POST['Password'],   
        request.POST['Confirm Password'])
        return render(request,'registration.html')
           
def login(request):
    return render(request,'login.html')
