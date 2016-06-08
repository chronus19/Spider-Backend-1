from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,HttpRequest,QueryDict
from django.core.exceptions import *
from string import (ascii_uppercase,ascii_lowercase,digits)
from random import choice
from validate_email import validate_email
from .models import Student
from exceptions import *      # Custom exceptions
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import re


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

        try:
            validate_data(data)                 # Validate input data
        except Exception as e:
            return render(req,'add.html',{'error':1,'errorMsg':e.message,})
        
        del data

        passcode = random_string();             # Generate random passcode

        try:                                    # Create an object (like adding a row to the Student's Table)
            obj = Student.objects.create(name=name,rollno=rollno,dept=dept,email=email,address=address,aboutme=aboutme,passcode=passcode);
        except ValidationError as e:            # If the object could not be created
            return render(req,'add.html',{'error':1,'errorMsg':e.message,})

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
                    return render(req,'view.html',{'error':1,'errorMsg':RollNoError.message,})

                if Student.objects.filter(rollno=rollno).exists():    
                    student = list(Student.objects.filter(rollno=rollno))[0]
                    data = {'name':student.name,'rollno':student.rollno,'dept':student.dept,'email':student.email,'address':student.address,'aboutme':student.aboutme,}
                    return render(req,'showprofile.html',data)
                else:               # Requested roll number does not exist
                    return render(req,'view.html',{'error':1,'errorMsg':NotFoundError.message,})
    else:
        return HttpResponse('<center><h1>View Students</h1></center>');


def edit_student(req):
    if req.method=='GET':       # For editing data, the existing fields of the form is populated with the stored data
          if not req.GET.__contains__('rollno'):    
                return redirect('/view/')
          rollno = req.GET.get('rollno','')
          if Student.objects.filter(rollno=rollno).exists():    # If Roll Number exists, open the 'Edit Student' Page
                student = list(Student.objects.filter(rollno=rollno))[0]
                data = {'name':student.name,'rollno':student.rollno,'dept':student.dept,'email':student.email,'address':student.address,'aboutme':student.aboutme,}
                return render(req,'edit.html',data)
          else:
                return redirect('/view/')
    elif req.method == 'POST':      # For updating data
        data = req.POST
        rollno = data.get('rollno','')
        passcode = data.get('passcode','')
        name = data.get('name','')
        dept = data.get('dept','')
        email = data.get('email','')
        address = data.get('address','')
        aboutme = data.get('aboutme','')

        try:
            validate_data(data,new_student=0)         # Validate input data
        except Exception as e:
            return render(req,'edit.html',{'error':1,'errorMsg':e.message,'name':name,'rollno':rollno,'dept':dept,'email':email,'address':address,'aboutme':aboutme,})

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
        student.save()              # Save the updated information about the student
        return redirect('/view/?rollno=' + rollno)   # Display updated information   

    else:
        return redirect('/view/')

def view_all(req):
    if req.method != 'GET':
        return redirect('/view_all/')

    page_no = req.GET.get('page','1')
    sortby = req.GET.get('sortby','')
    order = req.GET.get('order','')
    groupby = req.GET.get('groupby','')

    if sortby=='' and order=='' and req.session.__contains__('sortby') and req.session.__contains__('order'):
        sortby = req.session['sortby']
        order = req.session['order']
    if groupby =='' and req.session.__contains__('groupby'):
        groupby = req.session['groupby']
    elif groupby in ['CSE','MECH','CIVIL','ICE','CHEM','MME','PROD','ECE','EEE']:
        req.session['groupby'] = groupby
        
    if order in ['asc','dsc'] and sortby in ['rollno','name']:
        req.session['sortby'] = sortby
        req.session['order'] = order
        if order == 'dsc':
            sortby = '-' + sortby
        if groupby in ['CSE','MECH','CIVIL','ICE','CHEM','MME','PROD','ECE','EEE']:
            page_list = Paginator(Student.objects.filter(dept=groupby).order_by(sortby), 10)
        else:
            page_list = Paginator(Student.objects.all().order_by(sortby), 10)
    else:
        page_list = Paginator(Student.objects.all(), 10)
    
    try:
        page = page_list.page(page_no)
    except PageNotAnInteger:
        page = page_list.page(1)
    except EmptyPage:
        page = page_list.page(page_list.num_pages)
    
    return render(req,'view_all.html',{'all_students':page,})
    


def validate_data(data,new_student=1):        # Function for validating input data from user
    name = data.get('name','')
    rollno = data.get('rollno','')
    dept = data.get('dept','')
    email = data.get('email','')
    address = data.get('address','')
    aboutme = data.get('aboutme','')
    chars = ascii_uppercase + ascii_lowercase
    del data

    if re.search(r'[^a-zA-Z ]',name) is not None:
        raise NameError

    if not(rollno.isdigit()) or len(rollno)!=9:
        raise RollNoError
    
    if not email.endswith('@nitt.edu') or not validate_email(email):
        raise EmailError
    
    if len(address)<1 or len(address)>180:
        raise AddressError
    
    if len(aboutme)>500:
        raise AboutMeError
    
    if dept not in ['CSE','MECH','CIVIL','ICE','CHEM','MME','PROD','ECE','EEE']:
        raise DeptError

    if Student.objects.filter(rollno=rollno).exists() and new_student==1:
        raise ExistsError
    
    return 0    

    
def random_string(size=5):
    chars = ascii_uppercase + digits.replace('0','') # Selecting from, and to remove confusion b/w O and 0
    return ''.join(choice(chars) for _ in range(size))
