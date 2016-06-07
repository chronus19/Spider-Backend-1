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
            'ExistsError':'Roll number provided already exists','ServerError':'Some internal server error occured',
            'NotFoundError':'Requested Roll Number does not exist'}

def add_student(req):
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
                
        x = validate_data(data)         # Validate input data
        if x != 0:          
            return render(req,'add.html',{'error':x,'errorMsg':errorMsg.get(x,''),})
        del data

        if Student.objects.filter(rollno=rollno).exists():      # If Roll Number already exists
            return render(req,'add.html',{'error':'ExistsError','errorMsg':errorMsg.get('ExistsError',''),})

        passcode = random_string();             # Generate random passcode

        try:                            # Create an object (like adding a row to the Student's Table)
            obj = Student.objects.create(name=name,rollno=rollno,dept=dept,email=email,address=address,aboutme=aboutme,passcode=passcode);
        except ValidationError:         # If the object could not be created
            return render(req,'add.html',{'error':'ServerError','errorMsg':errorMsg.get('ServerError',''),})

        if obj is not None:
            return render(req,'success.html',{'passcode':passcode})     # Display a success page, with passcode      
        else:
            return render(req,"add.html");
    else:
        return render(req,'select.html')    

def view_student(req):
    if req.method=='GET':
          if not req.GET.__contains__('rollno'):    # If 'rollno' not in GET parameter
                return render(req,"view.html") 
          else:
                rollno = req.GET.get('rollno','')        
                if not(rollno.isdigit()) or len(rollno)!=9:     # Validate input roll number  
                    return render(req,'view.html',{'error':'RollNoError','errorMsg':errorMsg.get('RollNoError',''),})

                if Student.objects.filter(rollno=rollno).exists():    
                    student = list(Student.objects.filter(rollno=rollno))[0]
                    data = {'name':student.name,'rollno':student.rollno,'dept':student.dept,'email':student.email,'address':student.address,'aboutme':student.aboutme,}
                    return render(req,'showprofile.html',data)
                else:               # Requested roll number does not exist
                    return render(req,'view.html',{'error':'NotFoundError','errorMsg':errorMsg.get('NotFoundError',''),})
    else:
        return HttpResponse('<center><h1>View Students</h1></center>');

def edit_student(req):
    if req.method=='GET':       # For editing data
          if not req.GET.__contains__('rollno'):    
                return redirect('/view/')
          rollno = req.GET.get('rollno','')
          if Student.objects.filter(rollno=rollno).exists():    # If Roll Number exists, open the 'Edit Student' Page
                student = list(Student.objects.filter(rollno=rollno))[0]
                data = {'name':student.name,'rollno':student.rollno,'dept':student.dept,'email':student.email,'address':student.address,'aboutme':student.aboutme,}
                return render(req,'edit.html',data)
          else:
                return redirect('/view/')
    elif req.method == 'POST':  # For updating data
        data = req.POST
        rollno = data.get('rollno','')
        passcode = data.get('passcode','')
        name = data.get('name','')
        dept = data.get('dept','')
        email = data.get('email','')
        address = data.get('address','')
        aboutme = data.get('aboutme','')
                
        x = validate_data(data)     # Validate Input Data

        if x!=0:
            return render(req,'edit.html',{'error':x,'errorMsg':errorMsg.get(x,''),'name':name,'rollno':rollno,'dept':dept,'email':email,'address':address,'aboutme':aboutme,})

        # Checking if Roll number and Passcode match
        if not Student.objects.filter(rollno=rollno,passcode=passcode).exists():        
            return HttpResponse('<center> <h2> Invalid credentials !! <br> <a href="/view/?rollno=%s">View Student</a> </h2></center>' % rollno)

        # Roll number and passcode match
        student = Student.objects.get(rollno=rollno,passcode=passcode)
        student.name = name
        student.dept = dept
        student.email = email
        student.address = address
        student.aboutme = aboutme
        student.save()              # save the updated information about the student
        return redirect('/view/?rollno=' + rollno)   # Display updated information   

    else:
        return redirect('/view/')

def validate_data(data):        # Function for validating input data from user
    name = data.get('name','')
    rollno = data.get('rollno','')
    dept = data.get('dept','')
    email = data.get('email','')
    address = data.get('address','')
    aboutme = data.get('aboutme','')
    chars = ascii_uppercase + ascii_lowercase
    del data

    for i in name :
        if i not in chars + '. ':
            return 'NameError'

    if name.count('.') > len(name.split()) or len(name)<2:
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
