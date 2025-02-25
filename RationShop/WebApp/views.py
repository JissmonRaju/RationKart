from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Sum

from AdminApp.models import Stock, RationItems
from WebApp.models import BeneficiaryRegister, ContactDB, CartDB, ShopOwner, OrderDB
from AdminApp.views import index


# Create your views here.

def home(request):
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()
    stks = Stock.objects.all()
    return render(request, 'Home.html', {'stks': stks, 'details': details})


def products(request):
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()

    prod = RationItems.objects.all()
    return render(request, 'Products.html', {'prod': prod, 'details': details})


def signup_page(request):
    return render(request, 'SignUpPage.html')


def save_signup(request):
    if request.method == 'POST':
        u_name = request.POST.get('bname')
        ration_card = request.POST.get('rationcard')
        card_color = request.POST.get('cardcolor')
        u_mail = request.POST.get('bmail')
        u_mobile = request.POST.get('bmobile')
        u_pass = request.POST.get('bpass')
        fam_members = request.POST.get('members')
        obj = BeneficiaryRegister(U_Name=u_name, Ration_Card=ration_card, Card_Color=card_color, U_Mail=u_mail,
                                  U_Mobile=u_mobile,
                                  U_Pass=u_pass, Family_Members=fam_members
                                  )
        obj.save()
        return redirect(login_page)


def shop_signup(request):
    if request.method == 'POST':
        u_name = request.POST.get('sname')
        reg_num = request.POST.get('regnumber')
        s_mail = request.POST.get('smail')
        s_mobile = request.POST.get('smobile')
        s_pass = request.POST.get('spass')
        obj = ShopOwner(S_Name=u_name, Reg_Num=reg_num, S_Mail=s_mail,
                        S_Mobile=s_mobile,
                        S_Pass=s_pass
                        )
        obj.save()
        return redirect(login_page)


def shop_home(request):
    det = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()

    return render(request, 'ShopHome.html', {'det': det})


def login_page(request):
    return render(request, 'LoginPage.html')


def save_login(request):
    if request.method == 'POST':
        unam_e = request.POST.get('uname')
        pass_words = request.POST.get('pass')
        user = authenticate(username=unam_e, password=pass_words)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect(index)
        elif BeneficiaryRegister.objects.filter(Ration_Card=unam_e, U_Pass=pass_words).exists():
            request.session['Ration_Card'] = unam_e
            request.session['U_Pass'] = pass_words
            return redirect(home)
        elif ShopOwner.objects.filter(Reg_Num=unam_e, S_Pass=pass_words).exists():
            request.session['Reg_Num'] = unam_e
            request.session['S_Pass'] = pass_words
            return redirect(reverse('ShopHome'))
        else:
            return redirect(login_page)
    else:
        return redirect(login_page)


def log_out(request):
    if request.session.get('Ration_Card'):
        request.session.pop('Ration_Card', None)
        request.session.pop('U_Pass', None)

    elif request.session.get('Reg_Num'):
        request.session.pop('Reg_Num', None)
        request.session.pop('S_Pass', None)

    return redirect(login_page)


def contact_us(request):
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()
    shp = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    return render(request, 'ContactUs.html', {'details': details,'shp':shp})


def save_contact(request):
    if request.method == 'POST':
        n_ame = request.POST.get('FullName')
        e_mail = request.POST.get('Email')
        phn_num = request.POST.get('PhoneNumber')
        mess_age = request.POST.get('mesg')
        obj = ContactDB(F_Name=n_ame, C_Mail=e_mail, Phn_Num=phn_num, Mesg=mess_age)
        obj.save()
        return redirect(home)


def about_page(request):
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()

    shp = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    return render(request, 'AboutUs.html',{'details': details,'shp':shp})


def single_product(request, si_id):
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()

    sing = RationItems.objects.get(id=si_id)

    # Get beneficiary details
    prod = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()
    family_members = prod.Family_Members if (prod and prod.Family_Members) else 1

    # Check if item is already in the cart
    user_cart = CartDB.objects.filter(User_Name=request.session.get('Ration_Card'), Item_Name=sing).exists()
    already_in_cart = user_cart  # Pass this to the template

    # For Yellow card, the allocation is fixed for the household (not per person)
    if prod and prod.Card_Color == "Yellow":
        if sing.Ration == "Rice":
            final_quantity = 28
        elif sing.Ration == "Wheat":
            final_quantity = 7
        else:
            final_quantity = 35
    else:
        allocations = {
            "Pink": {"Rice": 4, "Wheat": 1},
            "Blue": {"Rice": 2},
            "White": {"Rice": 8.90, "Wheat": 6.70}
        }
        if prod and prod.Card_Color in allocations and sing.Ration in allocations[prod.Card_Color]:
            per_member_qty = allocations[prod.Card_Color][sing.Ration]
            final_quantity = per_member_qty * family_members
        else:
            product_defaults = {"Wheat": 3, "Boiled Rice": 5, "Matta Rice": 5, "Raw Rice": 7}
            default_quantity = product_defaults.get(sing.Ration, 1)
            final_quantity = default_quantity * family_members

    return render(request, 'SingleProduct.html', {
        'sing': sing,
        'prod': prod,
        'final_quantity': final_quantity,
        'already_in_cart': already_in_cart,
        'details': details
    })


def cart_page(request):
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()
    shp = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    if details:
        crt = CartDB.objects.filter(User_Name=request.session['Ration_Card'])
    elif shp:
        crt = CartDB.objects.filter(User_Name=request.session['Reg_Num'])
    else:
        crt = None
    ord = CartDB.objects.filter(User_Name=request.session.get('Ration_Card') or request.session.get('Reg_Num'))
    total_price = ord.aggregate(Sum('I_Total'))['I_Total__sum'] or 0
    quant = 0
    for i in crt:
        quant += i.Item_Quantity

    item_count = ord.count()

    return render(request, 'CartPage.html', {'crt': crt, 'details': details, 'shp': shp, 'total_price': total_price,'item_count':item_count,'quant':quant})


def save_cart(request):
    if request.session.get('Reg_Num'):
        if request.method == 'POST':
            i_name = request.POST.get('rname')
            usr_name = request.session.get('Reg_Num')
            i_price = request.POST.get('rprice')
            i_quant = request.POST.get('rquant')
            i_total = request.POST.get('rtotal')
            try:
                x = Stock.objects.get(Item=i_name)
                img = x.Item_Image
            except Stock.DoesNotExist:
                img = None
            if CartDB.objects.filter(User_Name=usr_name, Item_Name=i_name).exists():
                return redirect(shop_stock)
            obj = CartDB(
                User_Name=usr_name,
                Item_Name=i_name,
                Item_Quantity=int(i_quant),  # Ensure integer conversion
                I_Price=i_price,
                I_Total=i_total,
                Item_Image=img)
            obj.save()
        return redirect(shop_stock)
    elif request.session.get('Ration_Card'):
        if request.method == 'POST':
            i_name = request.POST.get('iname')
            usr_name = request.session.get('Ration_Card')
            i_price = request.POST.get('price')
            i_quant = request.POST.get('quant')
            i_total = request.POST.get('total')
            try:
                x = RationItems.objects.get(Ration=i_name)
                img = x.R_Image
            except RationItems.DoesNotExist:
                img = None
            if CartDB.objects.filter(User_Name=usr_name, Item_Name=i_name).exists():
                return redirect(products)
            obj = CartDB(
                User_Name=usr_name,
                Item_Name=i_name,
                Item_Quantity=int(i_quant),  # Ensure integer conversion
                I_Price=i_price,
                I_Total=i_total,
                Item_Image=img)
            obj.save()
        return redirect(products)


def delete_cart(request, crt_id):
    del_cart = CartDB.objects.filter(id=crt_id)
    del_cart.delete()
    return redirect(cart_page)


def sin_up(request):
    return render(request, 'ShopSignUp.html')


def my_details(request, my_id):
    details = BeneficiaryRegister.objects.filter(id=my_id).first()
    det = ShopOwner.objects.filter(id=my_id).first()

    return render(request, 'MyDetails.html', {'details': details, 'det': det})


def order_page(request):
    ration_card = request.session.get('Ration_Card')
    reg_num = request.session.get('Reg_Num')
    details = BeneficiaryRegister.objects.filter(Ration_Card=ration_card).first()
    shp = ShopOwner.objects.filter(Reg_Num=reg_num).first()
    ord = CartDB.objects.filter(User_Name=ration_card or reg_num)
    total_price = ord.aggregate(Sum('I_Total'))['I_Total__sum'] or 0
    item_count = ord.count()
    return render(request, 'OrderPage.html', {'details': details, 'ord': ord, 'shp': shp, 'total_price': total_price,
                                              'item_count': item_count})


def checkout_page(request):
    shp_ownr = request.session.get('Reg_Num')
    usr_cust = request.session.get('Ration_Card')
    ord = CartDB.objects.filter(User_Name=usr_cust or shp_ownr)
    total_price = ord.aggregate(Sum('I_Total'))['I_Total__sum'] or 0
    item_count = ord.count()
    if shp_ownr:
        chk = CartDB.objects.filter(User_Name=shp_ownr)
    elif usr_cust:
        chk = CartDB.objects.filter(User_Name=usr_cust)
    else:
        chk = None
    shp = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()

    return render(request, 'CheckOut.html', {'chk': chk,'details': details,'shp':shp,'total_price': total_price,
                                              'item_count': item_count})


def shop_stock(request):
    details = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    stks = Stock.objects.all()
    return render(request, 'ShopStock.html', {'details': details, 'stks': stks})


def shop_single_prod(request, s_id):
    details = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    singl = Stock.objects.get(id=s_id)
    produ = Stock.objects.all()
    return render(request, 'ShopSingleProd.html', {'singl': singl, 'produ': produ, 'details': details})


def shop_cart(request):
    return render(request, 'ShopCart.html')
