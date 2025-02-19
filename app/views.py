from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import numpy as np
import pickle
import os

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == 'POST':
        # Get data from form, ensuring keys match the form's name attributes exactly
        tenure = request.POST.get('tenure', '0')
        citytier = request.POST.get('citytier', '0')
        warehousetohome = request.POST.get('warehousetohome', '0')
        hourspendonapp = request.POST.get('hourspendonapp', '0')
        numberofdeviceregistered = request.POST.get('numberofdeviceregistered', '0')
        satisfactionscore = request.POST.get('satisfactionscore', '0')
        numberofaddress = request.POST.get('numberofaddress', '0')
        complain = request.POST.get('complain', '0')
        orderamounthikefromlastyear = request.POST.get('orderamounthikefromlastyear', '0')
        couponused = request.POST.get('couponused', '0')
        ordercount = request.POST.get('ordercount', '0')
        daysincelastorder = request.POST.get('daysincelastorder', '0')
        cashbackamount = request.POST.get('cashbackamount', '0')

        # Handle gender: Automatically allocate 0 or 1
        gender = request.POST.get('gender', 'Male')  # Default to 'Male' if not provided
        gender_female = 1 if gender.lower() == 'female' else 0
        gender_male = 1 if gender.lower() == 'male' else 0

        # Handle marital status: Automatically allocate 0 or 1
        maritalstatus = request.POST.get('maritalstatus', 'Single')  # Default to 'Single' if not provided
        maritalstatus_divorced = 1 if maritalstatus.lower() == 'divorced' else 0
        maritalstatus_married = 1 if maritalstatus.lower() == 'married' else 0
        maritalstatus_single = 1 if maritalstatus.lower() == 'single' else 0

        # Arrange features in the correct order as expected by the model
        features = [
            tenure, citytier, warehousetohome, hourspendonapp, numberofdeviceregistered,
            satisfactionscore, numberofaddress, complain, orderamounthikefromlastyear,
            couponused, ordercount, daysincelastorder, cashbackamount,
            gender_female, gender_male, 
            maritalstatus_divorced, maritalstatus_married, maritalstatus_single
        ]

        # Convert all inputs to float safely
        try:
            features = [float(i) for i in features]
        except ValueError:
            return render(request, 'app/index.html', {'error': 'Invalid input. Please enter valid numbers.'})
        features = np.array(features).reshape(1, -1)

        # Make prediction and calculate probability
        prediction_prob = model.predict_proba(features)[0][1]
        prediction_text = 'Churn' if prediction_prob > 0.4 else 'No Churn'

        return render(request, 'app/result.html', {'prediction': prediction_text, 'predict_probabality': round(prediction_prob, 4)})

    return render(request, 'app/index.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard/")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "app/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
            else:
                User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, "Account created successfully! Please log in.")
                return redirect("login")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "app/signup.html")

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "app/dashboard.html", {"username": request.user.username})

def segment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'app/segment.html')

def user_logout(request):
    logout(request)
    return redirect("login")

