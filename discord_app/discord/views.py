from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate , login as auth_login ,logout as auth_logout
from .models import User


def Home(request):
    return render(request , "home.html")

def nav(request):
    return render(request , "nav.html")

from django.shortcuts import render
from django.http import HttpResponse

def signup(request):
    if request.method == 'POST':
        # saving form value into variable
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        # print(fname,lname,username,email,password,confirm_password)

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                return HttpResponse("Username already exists")
            elif User.objects.filter(email=email).exists():
                return HttpResponse("Email already exists")
            else:
                # hashed_password = make_password(password)      # Making password in hased more secured

                # Make instance of User model class
                user = User(first_name=fname, last_name=lname, username=username, email=email, password=password )
                user.save()
                return HttpResponse("User created successfully")
        else:
            return HttpResponse("Passwords do not match")
    else:
        return render(request, 'signup.html')


# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

        
#         # Authenticate the user
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             auth_login(request, user)
#             return redirect('home')  # Redirect to home page or any other page
#         else:
#             # Invalid login credentials
#             return HttpResponse("Invalid username or password")
    
#     return render(request, 'login.html')

# def logout(request):
#     auth_logout(request)
#     return redirect('home')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect to home page or any other page
        else:
            # Invalid login credentials
            return HttpResponse("Invalid username or password")
    
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

