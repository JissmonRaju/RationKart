from django.contrib.auth import login
from django.shortcuts import render, redirect
from AdminApp.models import Stock
from WebApp.models import UserRegister,ContactDB


# Create your views here.

def home(request):
    stks = Stock.objects.all()
    return render(request, 'Home.html', {'stks': stks})


def products(request):
    prod = Stock.objects.all()
    return render(request, 'Products.html', {'prod': prod})


def signup_page(request):
    return render(request, 'SignUpPage.html')


def save_signup(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        ration_card = request.POST.get('rationcard')
        u_mail = request.POST.get('usermail')
        u_mobile = request.POST.get('usermobile')
        u_pass = request.POST.get('userpass')
        c_pass = request.POST.get('confirmpass')
        obj = UserRegister(U_Name=u_name, Ration_Card=ration_card, U_Mail=u_mail, U_Mobile=u_mobile, U_Pass=u_pass,
                           C_Pass=c_pass)
        obj.save()
        return redirect(login_page)


def login_page(request):
    return render(request, 'LoginPage.html')


def save_login(request):
    if request.method == 'POST':
        unam_e = request.POST.get('uname')
        pass_words = request.POST.get('pass')
        if UserRegister.objects.filter(U_Name=unam_e, U_Pass=pass_words).exists():
            request.session['U_Name'] = unam_e
            request.session['U_Pass'] = pass_words
            return redirect(home)
        else:
            return redirect(login_page)
    else:
        return redirect(login_page)


def log_out(request):
    del request.session['U_Name']
    del request.session['U_Pass']
    return redirect(login_page)


def contact_us(request):
    return render(request, 'ContactUs.html')

def save_contact(request):
    if request.method == 'POST':
        n_ame = request.POST.get('FullName')
        e_mail = request.POST.get('Email')
        phn_num = request.POST.get('PhoneNumber')
        mess_age = request.POST.get('mesg')
        obj = ContactDB(F_Name=n_ame,C_Mail=e_mail,Phn_Num=phn_num,Mesg=mess_age)
        obj.save()
        return redirect(home)

def about_page(request):
    return render(request,'AboutUs.html')

def cart_page(request):
    return render(request,'CartPage.html')