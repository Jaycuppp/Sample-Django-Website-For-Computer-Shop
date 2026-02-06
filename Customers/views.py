import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import *

from Website.views import *
from Website.cart import *
from Website.forms import *

def AccountPage(request):
    Form = None
    if request.user.is_authenticated: #As long as a logged in user is making a web request
        Current_User = User.objects.get(id=request.user.id)
        Form = UserUpdateForm(request.POST or None, instance=Current_User)
        
        if Form.is_valid():
            Form.save()
            login(request, Current_User)
            messages.success(request, "Your Account Has Been Updated!")
            return redirect("HomePage")
        
        else:
            return render(request, "Account_My_Account_Page.html", {"Form": Form, })
        
    else:
        messages.success(request, ("Error, You Must Be Logged In To Update Account Info!"))
        return redirect("HomePage")
    
def AccountPasswordReset(request):
    LoggedInUser = request.user

    if LoggedInUser.is_authenticated: #If the Web User has logged in to their established account
        if request.method == "POST": #If the User Hasn't Filled Out and Submitted the Form
            Form = UserUpdatePasswordForm(LoggedInUser, request.POST)
        
            if Form.is_valid(): #As long as the Form submission is valid
                Form.save() #Save the Form Submission
                messages.success(request, "Password Updated!")
                login(request, LoggedInUser) #Bonus Feature for keeping the user Logged In After Password Change
                return redirect("MyAccount")
        
                #Comment out the 2 lines above for the line below to work
                #return redirect("Login") #Requires Users to login with the New Password for Final Confirmation
        
            else: #If Form submission is NOT Valid
                for error in list(Form.errors.values()): #Grab all the Error Values from the Form
                    messages.error(request, error) #Post a Pop-up Error Message of the Form Error Values
                    return redirect("PasswordUpdate")
        else:
            Form = UserUpdatePasswordForm(LoggedInUser)
            return render(request, "Account_My_Account_Password_Update_Page.html", {"Form": Form})
    
    else:
        messages.success(request, "You Must Be Logged In To Your Account!")
        return render(request, "LoginPage.html", {})
    

def AccountProfileUpdate(request):
    if request.user.is_authenticated: #As long as a logged in user is making a web request
        current_user = WebsiteAccounts.objects.get(Web_User__id=request.user.id) #The Currently Logged In User`s ID 
        current_user_shipping = Customer_Shipping.objects.get(id=request.user.id) #Acquire the current logged in user`s shipping information
        Form = UserProfileForm(request.POST or None, instance=current_user) #As long as there is a Web User Instace, create the Form
        ShippingForm = Customer_Shipping_Form(request.POST or None, instance=current_user_shipping)
        
        if Form.is_valid(): 
            Form.save()
            ShippingForm.save()
            messages.success(request, ("Your Account Info Has Been Updated!"))
            return redirect("HomePage")
        
        else:
            return render(request, "Account_My_Account_Profile_Update_Page.html", {"Form": Form, "ShippingForm": ShippingForm,})
    else:
        messages.success(request, ("Error, You Must Be Logged In To Update Account Info!"))
        return redirect("HomePage")
    
    
def MySupport(request):
    return render(request, "Account_My_Support_Page.html", {})

def Login_Auth(request):
    if request.method == "POST": #Determines whether the User is logged in or not
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Code Below for User Cart Persistance
            Current_User = WebsiteAccounts.objects.get(Web_User__id=request.user.id) #Geting The Current User
            Saved_Cart = Current_User.Old_Cart #Getting the Cart String Value from the User`s Account
            if Saved_Cart: # As long as there is a Value for the Current` User`s Shop Cart
                Better_Cart = json.loads(Saved_Cart) #Using JSON Library, convert the Saved_Cart string back into a Pythonic Dict 
                New_Cart = Cart(request)
                for Key, Val in Better_Cart.items():
                    New_Cart.data_base_add(product=Key, quantity=Val)
        
            messages.success(request, ("You have Logged in successfully!"))
            return redirect("HomePage")
        
        else:
            messages.success(request, ("There was a Login error. Try again."))
            return redirect("LoginPage")
        
    else:
        return render(request, "Login.html", {})
    
    
def User_Logout(request):
    logout(request)
    messages.success(request, ("You have logged out!"))
    return redirect("HomePage")

def User_Register(request):
    if request.method == "POST":
        Form = UserRegistrationForm(request.POST)
        
        if Form.is_valid():
            Form.save()
            username = Form.cleaned_data["username"]
            password = Form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("Account successfully Created!"))
            return redirect ("LoginPage")      
        
    else:
        Form = UserRegistrationForm()               

    return render(request, "User_Register.html", {'Form': Form,})