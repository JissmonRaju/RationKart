from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from AdminApp.models import Stock, StockCategory
from django.contrib.auth.models import User
from WebApp.models import ContactDB,BeneficiaryRegister




# Create your views here.

def index(request):
    return render(request, 'Index.html')






def display_user(request):
    us_er = BeneficiaryRegister.objects.all()
    return render(request, 'Display_User.html', {'us_er': us_er})




def delete_user(request, u_id):
    del_usr = BeneficiaryRegister.objects.filter(id=u_id)
    del_usr.delete()
    return redirect(display_user)


def add_category(request):
    return render(request, 'Add_Category.html')


def save_category(request):
    if request.method == 'POST':
        c_name = request.POST.get('cname')
        c_desc = request.POST.get('cdesc')
        c_image = request.FILES['cimage']
        obj = StockCategory(Category_Name=c_name, C_Description=c_desc,Category_Image=c_image)
        obj.save()
        return redirect(add_category)


def display_category(request):
    cate = StockCategory.objects.all()
    return render(request, 'Display_Category.html', {'cate': cate})


def edit_category(request, c_id):
    cate = StockCategory.objects.get(id=c_id)
    return render(request, 'Edit_Category.html', {'cate': cate})


def update_category(request, c_id):
    if request.method == 'POST':
        c_name = request.POST.get('cname')
        c_desc = request.POST.get('cdesc')
        try:
            img = request.FILES['cimage']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = Stock.objects.get(id=c_id).Item_Image
        StockCategory.objects.filter(id=c_id).update(Category_Name=c_name, C_Description=c_desc,Category_Image=file)
        return redirect(display_category)


def delete_category(request, c_id):
    del_cat = StockCategory.objects.filter(id=c_id)
    del_cat.delete()
    return redirect(display_category)


def add_stock(request):
    cate = StockCategory.objects.all()
    return render(request, 'Add_Stock.html',{'cate':cate})


def save_stock(request):
    if request.method == 'POST':
        i_name = request.POST.get('iname')
        i_desc = request.POST.get('idesc')
        t_quant = request.POST.get('tquant')
        cate = request.POST.get('category')
        availability = request.POST.get('avail')
        i_price = request.POST.get('iprice')
        i_image = request.FILES['iimage']
        obj = Stock(Item=i_name, Description=i_desc, Total_Quantity=t_quant, Category=cate, Availability=availability,
                    Item_Price=i_price, Item_Image=i_image)
        obj.save()
        return redirect(add_stock)


def display_stock(request):
    stk = Stock.objects.all()
    return render(request, 'Display_Stock.html', {'stk': stk})


def edit_stock(request, s_id):
    edstk = Stock.objects.get(id=s_id)
    cate = StockCategory.objects.all()
    return render(request, 'Edit_Stock.html', {'edstk': edstk, 'cate': cate})


def update_stock(request, s_id):
    if request.method == 'POST':
        i_name = request.POST.get('iname')
        i_desc = request.POST.get('idesc')
        t_quant = request.POST.get('tquant')
        cate = request.POST.get('category')
        availability = request.POST.get('avail')
        i_price = request.POST.get('iprice')
        try:
            img = request.FILES['iimage']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = Stock.objects.get(id=s_id).Item_Image
        Stock.objects.filter(id=s_id).update(Item=i_name, Description=i_desc, Total_Quantity=t_quant, Category=cate,
                                             Availability=availability,Item_Price=i_price,
                                             Item_Image=file)
        return redirect(display_stock)


def delete_stock(request, s_id):
    del_stk = Stock.objects.filter(id=s_id)
    del_stk.delete()
    return redirect(display_stock)


def admin_login_page(request):
    return render(request,'Admin_Login.html')

def admin_login(request):
    if request.method=='POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        if User.objects.filter(username__contains=user_name).exists():
            var =authenticate(username=user_name,password=pass_word)
            if var is not None:
                login(request,var)
                request.session['username']=user_name
                request.session['password']=pass_word
                return redirect(index)
            else:
                return redirect(admin_login_page)
        else:
            return redirect(admin_login_page)


def admin_logout(request):
    del request.session['username']
    del request.session['password']
    return redirect(admin_login_page)


def view_message(request):
    msg = ContactDB.objects.all()
    return render(request,'ViewMsg.html',{'msg':msg})

def delete_message(request,m_id):
    del_msg = ContactDB.objects.filter(id=m_id)
    del_msg.delete()
    return redirect(view_message)
