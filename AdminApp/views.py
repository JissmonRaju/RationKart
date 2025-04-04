from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from AdminApp.models import Stock, StockCategory,RationItems
from django.contrib.auth.models import User
from WebApp.models import ContactDB, BeneficiaryRegister, OrderDB, Delivery, ShopOwner


# Create your views here.

def index(request):
    return render(request, 'Index.html')



def display_user(request):
    us_er = BeneficiaryRegister.objects.all()
    return render(request, 'Display_User.html', {'us_er': us_er})


def delete_user(request, u_id):
    del_usr = get_object_or_404(BeneficiaryRegister, id=u_id)

    if del_usr.user:  # Ensure there's an associated user
        del_usr.user.delete()

    # Delete the Beneficiary record
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



def add_ration(request):
    return render(request,'AddRation.html')

def save_ration(request):
    if request.method=='POST':
        r_name = request.POST.get('rname')
        r_desc = request.POST.get('rdesc')
        r_quant = request.POST.get('rquant')
        r_price = request.POST.get('rprice')
        r_avail = request.POST.get('ravail')
        r_image = request.FILES['rimage']
        obj = RationItems(Ration=r_name,R_Desc=r_desc,R_Quant=r_quant,R_Avail=r_avail,R_Price=r_price,R_Image=r_image)
        obj.save()
        return redirect(add_ration)

def display_ration(request):
    rat = RationItems.objects.all()
    return render(request,'Display_Ration.html',{'rat':rat})

def edit_ration(request,r_id):
    rt = RationItems.objects.get(id=r_id)
    return render(request,'Edit_Ration.html',{'rt':rt})

def update_ration(request,r_id):
    if request.method == 'POST':
        r_name = request.POST.get('rname')
        r_desc = request.POST.get('rdesc')
        r_quant = request.POST.get('rquant')
        r_price = request.POST.get('rprice')
        r_avail = request.POST.get('ravail')
        try:
            img = request.FILES['rimage']
            fs = FileSystemStorage()
            file = fs.save(img.name,img)

        except MultiValueDictKeyError:
            file = RationItems.objects.get(id=r_id).R_Image

        RationItems.objects.filter(id=r_id).update(Ration=r_name,R_Desc=r_desc,R_Quant=r_quant,R_Avail=r_avail,R_Price=r_price,R_Image=file)
        return redirect(display_ration)

def del_ration(request,r_id):
    delete_ration = RationItems.objects.filter(id=r_id)
    delete_ration.delete()
    return redirect(display_ration)


def order_details(request):
    ord_det = OrderDB.objects.all()
    return render(request,'Order_Details.html',{'ord_det':ord_det})

def del_orders(request,o_id):
    del_ord = OrderDB.objects.filter(id=o_id)
    del_ord.delete()
    return redirect(order_details)


def view_delivery(request):
    dp = Delivery.objects.all()
    return render(request, 'DisplayDelivery.html', {'dp': dp})


def del_partner(request, p_id):
    delete_partner = Delivery.objects.filter(id=p_id).first()
    if delete_partner and delete_partner.D_Partner:
        delete_partner.D_Partner.delete()  # Delete the linked User
    delete_partner.delete()  # Then delete the Delivery partner entry
    return redirect(view_delivery)


def view_shops(request):
    sh = ShopOwner.objects.all()
    return render(request, 'View_Owners.html', {'sh': sh})


def del_shop(request, s_id):
    delete_shp = ShopOwner.objects.filter(id=s_id).first()
    if delete_shp and delete_shp.user:
        delete_shp.user.delete()  # This deletes the associated User
    delete_shp.delete()  # Then delete the ShopOwner entry
    return redirect(view_shops)
