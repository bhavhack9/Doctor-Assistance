from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.db.models import Q,Max
from django.db import transaction

from . import initialPrediction, finalprediction
from .models import *
from .forms import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from datetime import datetime

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

from sklearn.ensemble import RandomForestClassifier
import json

from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'auth/login.html')    

def logout(request):
    request.session.clear()
    return redirect('index')

def register(request):
    return render(request,'auth/register.html')

def forgotPassword_view(request):
    return render(request,'auth/forgot_password.html')

def createAccount(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = form.save()
            response = {
                'status': True,
                'message': 'User Created Successfully'
            }
            return JsonResponse(response)
        else:
            # Form is not valid, extract error messages
            errors = form.errors
            print(errors)
            error_message = str(errors['contact'][0]) if 'contact' in errors else str(errors['email'][0]) if 'email' in errors else str(errors['usn_number'][0]) if 'usn_number' in errors else 'Invalid form data'

            response = {
                'status': False,
                'message': error_message
            }
            return JsonResponse(response)

def loginAccount(request):
    if request.method=='POST': 
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email, password=password,is_active=1).first()

        if user is None :
            response={
                'status':False,
                'message':'Invalid User'
            }
        else:
            request.session['user']=user.id
            request.session['user_type']=user.user_type
            response={
                'status':True,
                'message':'Successfully logged in'
            }
           
    return JsonResponse(response)

def home_view(request):
    if 'user' not in request.session and 'user_type' not in request.session:
        return redirect('logout')

    return render(request,'home/home.html')

def backup_password(request):
    if request.method == 'POST':

        email= request.POST['email']
        user = User.objects.filter(email=email).first()
        if user and user is not None:
             subject = 'Password backup'
             message = f'Password of your Doctor Assistance application is : {user.password}'
             from_email = 'doctorassistance@gmail.com'
             recipient_list = [user.email]
             send_mail(subject, message, from_email, recipient_list, fail_silently=False)
             response = {
                'status': True,
                'message': 'Your  password has been Successfully sent to your email address'
             }
        else:
            response = {
                'status': False,
                'message': 'Invalid email id'
            }     
    return JsonResponse(response)   

def admin_doctor(request):
    if 'user' not in request.session and 'user_type' not in request.session:
        return redirect('logout')

    if request.method == 'POST':  
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            response = { 
                'status': True,
                'message': 'Record Created Successfully'
            }
            return JsonResponse(response)
        else:
            # Form is not valid, extract error messages
            errors = form.errors
            print(errors)
            error_message = str(errors['contact'][0]) if 'contact' in errors else str(errors['email'][0]) if 'email' in errors else str(errors['usn_number'][0]) if 'usn_number' in errors else 'Invalid form data'

            response = {
                'status': False,
                'message': error_message
            }
            return JsonResponse(response)

    doctors = Doctor.objects.all().order_by('-id')
    return render(request,'home/admin/doctor.html',{'doctors':doctors})

def chatbot(request):
    user_id = request.session['user']
    user_instance = User.objects.filter(id=user_id).first()
    return render(request,'home/user/chatbot.html',{'user':user_instance})


# Predicting the initial Diseases
@csrf_exempt
def predict_initial_disease(request):
    symptoms=request.POST.get('response')
    symptoms = json.loads(symptoms)
    result=initialPrediction.predict(symptoms[0])
    result=remove_repeated_disease_names(result)

    response = {
        'status': True,
        'message':result
    }
    return JsonResponse(response)
def remove_repeated_disease_names(data):
    result = []
    for entry in data:
        parts = entry.split(', ')
        disease = parts[0]
        unique_symptoms = [disease]
        seen = set([disease])
        for part in parts[1:]:
            if part not in seen:
                unique_symptoms.append(part)
                seen.add(part)
        result.append(', '.join(unique_symptoms))
    return result

@csrf_exempt
def predict_disease(request):
    if 'user' not in request.session and 'user_type' not in request.session:
        return redirect('logout')

    res = request.POST.get('response')
    y_predicted=finalprediction.predict(res)
# =========================================================================
    if request.method == 'POST':


        user_id = request.session['user']
        user_instance = User.objects.filter(id=user_id).first()


        if user_instance:
            dob_str = user_instance.dob.strftime("%Y-%m-%d")  # Convert dob to string
            birth_date = datetime.strptime(dob_str, "%Y-%m-%d")  # Convert to datetime
            age = calculate_age(birth_date)

            gender = user_instance.gender

            if gender == "Male":
                gender = 2
            else:
                gender = 1


            doctor_instance = Doctor.objects.filter(specialization=y_predicted[0],is_active=1)

            if doctor_instance:
                serializer = DoctorSerializer(doctor_instance, many=True)
                if serializer.data:
                    response ={
                        'status': True,
                        'message': y_predicted[0],
                        'probability':y_predicted[1],
                        'data':serializer.data,

                    }
                    return JsonResponse(response)
            else:
                response ={
                    'status': False,
                    'message': y_predicted[0],
                    'probability': y_predicted[1]
                }
                return JsonResponse(response)

    return render(request,'home/user/chatbot.html',{'user':user_instance})


# @csrf_exempt
# def predict_disease(request):
#     if 'user' not in request.session and 'user_type' not in request.session:
#         return redirect('logout')
#
#     dataset=pd.read_csv('dataset.csv')
#     dataset = dataset.replace({'Yes': 1, 'No': 0,'Female':1,'Male':2,'Low':1,'Normal':2,'High':3})
#     dataset.shape
#
#     X=np.array(dataset.iloc[:,:-1])
#     X=X.astype(dtype='int')
#     Y=np.array(dataset.iloc[:,-1])
#     Y=Y.reshape(-1,)
#
#     X_train, X_test, y_train, y_test =train_test_split(X,Y,test_size=0.25,random_state=42)
#     print("X_train.shape",X_train.shape)
#     model_disease=RandomForestClassifier(n_estimators=100,criterion='entropy',)
#     model_disease.fit(X_train,y_train)
#
#     if request.method == 'POST':
#         user_id = request.session['user']
#         user_instance = User.objects.filter(id=user_id).first()
#
#         my_list_json = request.POST.get('response')
#         X_test = json.loads(my_list_json)
#
#         if user_instance:
#             dob_str = user_instance.dob.strftime("%Y-%m-%d")  # Convert dob to string
#             birth_date = datetime.strptime(dob_str, "%Y-%m-%d")  # Convert to datetime
#             age = calculate_age(birth_date)
#
#             gender = user_instance.gender
#
#             if gender == "Male":
#                 gender = 2
#             else:
#                 gender = 1
#
#             X_test.insert(4, age)
#             X_test.insert(5, gender)
#
#             print(X_test)
#             # X_test = [1,0,1,1,19,1,1,2]
#             y_predicted=model_disease.predict(np.asarray(X_test).reshape(1,-1))
#
#             print(y_predicted[0])
#
#             doctor_instance = Doctor.objects.filter(specialization=y_predicted[0],is_active=1)
#
#             if doctor_instance:
#                 serializer = DoctorSerializer(doctor_instance, many=True)
#                 if serializer.data:
#                     response ={
#                         'status': True,
#                         'message': y_predicted[0],
#                         'data':serializer.data,
#                         'data_list':X_test
#                     }
#                     return JsonResponse(response)
#             else:
#                 response ={
#                     'status': False,
#                     'message': y_predicted[0],
#                     'data_list':X_test
#                 }
#                 return JsonResponse(response)
#
#     return render(request,'home/user/chatbot.html',{'user':user_instance})



def calculate_age(birth_date):
    # Get the current date
    current_date = datetime.now()
    # Calculate the age
    age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
    return age



def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html_content = template.render(context_dict)
    return html_content.encode('utf-8')

def generate_pdf_view(request):
    print("heloooooooooooooooooooooooooooooooo")
    questions = request.GET.get('questions')
    answers = request.GET.get('answers')
    disease = request.GET.get('disease')
    probability=request.GET.get('probability')
    print("prob:",probability)
    
    if questions and answers:
        # Deserialize the serialized lists back into Python lists
        list1 = json.loads(questions)
        list2 = json.loads(answers)
        list1 = list1[1:]

    user_id = request.session['user']
    user_instance = User.objects.filter(id=user_id).first()
    
    data = [{'question': q, 'answer': a} for q, a in zip(list1, list2)]
    template_path = 'components/medical_report.html'
    html_bytes = render_to_pdf(template_path, {'data': data,'disease':disease,'prob':probability,'user':user_instance})

    result = BytesIO()
    try:
        print("Calling pisa.pisaDocument...")
        pdf = pisa.pisaDocument(BytesIO(html_bytes), result)
        print("pisa.pisaDocument call successful")
    except Exception as e:
        print(f"Error calling pisa.pisaDocument: {e}")
        return HttpResponse("Error generating PDF", status=400)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="medical_report.pdf"'
        return response
    else:return HttpResponse("Error generating PDF", status=400)
