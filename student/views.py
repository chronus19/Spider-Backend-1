from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,HttpRequest,QueryDict
from django.core.exceptions import *
from string import (ascii_uppercase,ascii_lowercase,digits)
from random import choice
from validate_email import validate_email
from .models import Student

errorMsg = {'NameError':'Enter appropriate name','RollNoError':'Enter valid Roll Number',\
            'EmailError':'Enter valid e-mail address','AddressError':'No. of characters in \'Address\' should be between 1-180',\
            'AboutMeError':'\'About me\' should have less than 500 characters','DeptError':'Enter a valid department',\
            'ExistsError':'Roll number provided already exists','ServerError':'Some internal server error occured',}

def add(req):
    if req.method=='GET':
        return render(req,"add.html");
    elif req.method=='POST':
        data = req.POST
        name = data.get('name','')
        rollno = data.get('rollno','')
        dept = data.get('dept','')
        email = data.get('email','')
        address = data.get('address','')
        aboutme = data.get('aboutme','')
                
        x = validate_data(data)
        if x != 0:
            return render(req,'add.html',{'error':x,'errorMsg':errorMsg.get(x,''),})
        del data

        if Student.objects.filter(rollno=rollno).exists():
            return render(req,'add.html',{'error':'ExistsError','errorMsg':errorMsg.get('ExistsError',''),})

        passcode = random_string();

        try:
            obj = Student.objects.create(name=name,rollno=rollno,dept=dept,email=email,address=address,aboutme=aboutme,passcode=passcode);
        except ValidationError:
            return render(req,'add.html',{'error':'ServerError','errorMsg':errorMsg.get('ServerError',''),})
        if obj is not None:
            return render(req,'success.html',{'passcode':passcode})       
        else:
            return render(req,"add.html");
    else:
        return render(req,'select.html')

def view(req):
    # To be worked upon shortly
    return HttpResponse('<center><h1>View Students</h1></center>');

def validate_data(data):
    name = data.get('name','')
    rollno = data.get('rollno','')
    dept = data.get('dept','')
    email = data.get('email','')
    address = data.get('address','')
    aboutme = data.get('aboutme','')
    chars = ascii_uppercase + ascii_lowercase
    del data

    f = 0
    
    for i in name :
        if i not in chars + '. ':
            return 'NameError'
    for i in name:
        if i in chars:
            f=1
            break
    if f==0:
        return 'NameError'
    
    if not(rollno.isdigit()) or len(rollno)!=9:
        return 'RollNoError'
    
    if email[-9:] != '@nitt.edu' or not validate_email(email):
        return 'EmailError'
    
    if len(address)<1 or len(address)>180:
        return 'AddressError'
    
    if len(aboutme)>500:
        return 'AboutMeError'
    
    if dept not in ['CSE','MECH','CIVIL','ICE','CHEM','MME','PROD','ECE','EEE']:
        return 'DeptError'
    
    return 0
    
def random_string(size=5):
    chars = ascii_uppercase + digits.replace('0','') # Selecting from, and to remove confusion b/w O and 0
    return ''.join(choice(chars) for _ in range(size))
