from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from AdminApp.models import Stock
from WebApp.models import BeneficiaryRegister, ContactDB, CartDB, ShopOwner
from AdminApp.views import index


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
        elif BeneficiaryRegister.objects.filter(U_Name=unam_e, U_Pass=pass_words).exists():
            request.session['U_Name'] = unam_e
            request.session['U_Pass'] = pass_words
            return redirect(home)
        elif ShopOwner.objects.filter(S_Name=unam_e, S_Pass=pass_words).exists():
            request.session['S_Name'] = unam_e
            request.session['S_Pass'] = pass_words
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
        obj = ContactDB(F_Name=n_ame, C_Mail=e_mail, Phn_Num=phn_num, Mesg=mess_age)
        obj.save()
        return redirect(home)


def about_page(request):
    return render(request, 'AboutUs.html')


def single_product(request, si_id):
    sing = Stock.objects.get(id=si_id)

    # Get beneficiary details
    prod = BeneficiaryRegister.objects.filter(U_Name=request.session.get('U_Name')).first()
    family_members = prod.Family_Members if (prod and prod.Family_Members) else 1

    # For Yellow card, the allocation is fixed for the household (not per person)
    if prod and prod.Card_Color == "Yellow":
        if sing.Item == "Rice":
            final_quantity = 28  # Total household allocation for Rice under Yellow card
        elif sing.Item == "Wheat":
            final_quantity = 7  # Total household allocation for Wheat under Yellow card
        else:
            final_quantity = 35  # Default household allocation for other items
    else:
        # For other cards, allocations are given on a per-person basis.
        # Pink card now supports both Rice and Wheat selections.
        allocations = {
            "Pink": {"Rice": 4, "Wheat": 1},
            "Blue": {"Rice": 2},
            "White": {"Rice": 8.90, "Wheat": 6.70}
        }
        if prod and prod.Card_Color in allocations and sing.Item in allocations[prod.Card_Color]:
            per_member_qty = allocations[prod.Card_Color][sing.Item]
            final_quantity = per_member_qty * family_members
        else:
            # Fallback: For products not covered above, use default per-person allocation then multiply
            product_defaults = {
                "Wheat": 3,
                "Boiled Rice": 5,
                "Matta Rice": 5,
                "Raw Rice": 7
            }
            default_quantity = product_defaults.get(sing.Item, 1)
            final_quantity = default_quantity * family_members

    return render(request, 'SingleProduct.html', {
        'sing': sing,
        'prod': prod,
        'final_quantity': final_quantity
    })


def cart_page(request):
    crt = CartDB.objects.filter(User_Name=request.session['U_Name'])
    return render(request, 'CartPage.html', {'crt': crt})


def save_cart(request):
    if request.method == 'POST':
        i_name = request.POST.get('iname')
        usr_name = request.POST.get('usrname')
        i_price = request.POST.get('price')
        i_quant = request.POST.get('quant')
        i_total = request.POST.get('total')
        try:
            x = Stock.objects.get(Item=i_name)
            img = x.Item_Image
        except Stock.DoesNotExist:
            img = None
        obj = CartDB(
            User_Name=usr_name,
            Item_Name=i_name,
            Item_Quantity=int(i_quant),  # Ensure integer conversion
            I_Price=int(i_price),
            I_Total=int(i_total),
            Item_Image=img)
        obj.save()
        return redirect(products)


def delete_cart(request, crt_id):
    del_cart = CartDB.objects.filter(id=crt_id)
    del_cart.delete()
    return redirect(cart_page)


def sin_up(request):
    return render(request, 'ShopSignUp.html')


def my_details(request):
    details = BeneficiaryRegister.objects.all()
    return render(request, 'MyDetails.html', {'details': details})
