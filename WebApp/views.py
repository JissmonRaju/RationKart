
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db.models import Sum
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from .decorators import approval_required
import json
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.timezone import now
from .models import ShopOwner, OTPVerification
from .utils import generate_otp, send_otp_email
from django.utils.timezone import now
from django.db.models import Q
from AdminApp.models import Stock, RationItems
from WebApp.models import BeneficiaryRegister, ContactDB, CartDB, ShopOwner, OrderDB, OrderStatus, Delivery
from django.contrib import messages
from django.db import IntegrityError
import AdminApp.models
import razorpay
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from WebApp.models import BeneficiaryRegister, ShopOwner
from django.contrib.auth.models import User



# Create your views here.

def home(request):
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()
    cart_count = CartDB.objects.filter(User_Name=request.session.get('Ration_Card'), order__isnull=True)
    x = cart_count.count()
    stks = Stock.objects.all()
    dev = Delivery.objects.all()
    return render(request, 'Home.html', {'stks': stks, 'details': details, 'x': x, 'dev': dev})


def products(request):
    cart_count = CartDB.objects.filter(User_Name=request.session['Ration_Card'], order__isnull=True)
    x = cart_count.count()
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()

    prod = RationItems.objects.all()
    return render(request, 'Products.html', {'prod': prod, 'details': details, 'x': x})


def shop_home(request):
    reg_num = request.session.get('Reg_Num')
    det = ShopOwner.objects.filter(Reg_Num=reg_num).first()
    cart_count = CartDB.objects.filter(User_Name=reg_num, order__isnull=True)
    x = cart_count.count()
    return render(request, 'ShopHome.html', {'det': det, 'x': x})


# --- Beneficiary Side ---

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
        shp_id = request.POST.get('regnum')
        c_pass = request.POST.get('cpass')
        print("Shop ID received:", shp_id)  # Debug check

        try:
            # Create user (using ration card as username)
            user = User.objects.create_user(username=ration_card, password=u_pass)
            # Create beneficiary record with is_approved=False
            BeneficiaryRegister.objects.create(
                user=user,
                U_Name=u_name,
                Ration_Card=ration_card,
                Card_Color=card_color,
                U_Mail=u_mail,
                U_Mobile=u_mobile,
                Family_Members=fam_members,
                Shop_ID=shp_id,
                C_Pass=c_pass,
                is_approved=False
            )
            messages.success(request, "Signup submitted! Your account is pending approval.")
            login(request, user)
            return redirect('PendingApproval')
        except IntegrityError:

            print(BeneficiaryRegister.objects.filter(Shop_ID='YOUR_RATION_CARD_NUMBER').exists())
            messages.error(request, "Ration Card number already exists.")
            return redirect('SignUpPage')

    return redirect('SignUpPage')


def pending_approval(request):
    """
    Page shown to beneficiaries after signup, informing them their account is pending.
    """
    return render(request, 'PendingApproval.html')


# --- Shop Owner Side ---

@login_required
def pending_requests(request):
    """
    View for shop owners to see pending beneficiary signups for their shop.
    """
    if hasattr(request.user, 'shopowner_profile'):
        shop_id = request.user.shopowner_profile.Reg_Num
        pending_beneficiaries = BeneficiaryRegister.objects.filter(
            Shop_ID=shop_id, is_approved=False
        )
        # Debug logs:
        print("Logged-in ShopOwner Reg_Num:", shop_id)
        print("Pending Beneficiaries:", pending_beneficiaries)
        return render(request, 'ApproveRequest.html', {
            'pending_beneficiaries': pending_beneficiaries
        })
    return redirect('PendingApproval')


@csrf_exempt
@login_required
def approve_beneficiary(request, beneficiary_id):
    """
    Process shop owner’s approval for a beneficiary and redirect them to the approve requests page.
    """
    if request.method == 'POST' and hasattr(request.user, 'shopowner_profile'):
        beneficiary = BeneficiaryRegister.objects.filter(
            id=beneficiary_id, is_approved=False
        ).first()

        if beneficiary and beneficiary.Shop_ID == request.user.shopowner_profile.Reg_Num:
            beneficiary.is_approved = True
            beneficiary.save()
            # Store approval status in session for customer to check (if needed)
            request.session['approved_beneficiary_id'] = beneficiary.id

            messages.success(request, f"{beneficiary.U_Name} has been approved.")
            return redirect('ApproveRequests')

    return redirect('ApproveRequests')


def check_approval_status(request):
    print("DEBUG: check_approval_status for user:", request.user.username)
    if request.user.is_authenticated and hasattr(request.user, 'beneficiary_profile'):
        beneficiary = request.user.beneficiary_profile
        print("DEBUG: beneficiary.id =", beneficiary.id, "approved =", beneficiary.is_approved)
        if beneficiary.is_approved:
            return JsonResponse({'is_approved': True, 'beneficiary_id': beneficiary.id})
    return JsonResponse({'is_approved': False})


@csrf_exempt
@login_required
def reject_beneficiary(request, beneficiary_id):
    """
    Process rejection of a beneficiary signup.
    """
    if request.method == 'POST' and hasattr(request.user, 'shopowner_profile'):
        beneficiary = BeneficiaryRegister.objects.filter(
            id=beneficiary_id, is_approved=False
        ).first()
        if beneficiary and beneficiary.Shop_ID == request.user.shopowner_profile.Reg_Num:
            beneficiary.delete()
            messages.success(request, f"{beneficiary.U_Name}'s request has been rejected.")
    return redirect('ApproveRequests')


def final_status(request, beneficiary_id):
    beneficiary = get_object_or_404(BeneficiaryRegister, id=beneficiary_id)
    # Decide the status based on beneficiary.is_approved (for now, if not approved, we assume rejected)
    status = "approved" if beneficiary.is_approved else "rejected"
    return render(request, 'Approved.html', {
        'beneficiary': beneficiary,
        'status': status,
    })


# --- Login ---

def login_page(request):
    return render(request, 'LoginPage.html')


def save_login(request):
    if request.method == 'POST':
        uname_e = request.POST.get('uname')
        pass_words = request.POST.get('pass')
        user = authenticate(username=uname_e, password=pass_words)

        if user is not None:
            print("DEBUG: Logging in user:", user.username)
            # For beneficiaries, allow login even if not approved,
            # but then redirect them to the pending approval page.
            if hasattr(user, 'beneficiary_profile'):
                shop_owner = ShopOwner.objects.filter(Reg_Num=user.beneficiary_profile.Shop_ID).first()
                print("DEBUG: Setting session Ration_Card:", user.beneficiary_profile.Ration_Card)
                request.session['Ration_Card'] = user.beneficiary_profile.Ration_Card
                login(request, user)
                if not user.beneficiary_profile.is_approved:
                    messages.info(request, "Your account is pending approval. Please wait.")
                    return redirect('PendingApproval')
                else:
                    messages.success(request, "Login Success")
                    # If approved, redirect to final status page.
                    return redirect('Home')

            # For shop owners and other roles:
            login(request, user)
            if hasattr(user, 'delivery_profile'):
                request.session['delivery_partner'] = user.username
                messages.success(request, "Login Success")
                return redirect('Delivery_Partner')
            if hasattr(user, 'shopowner_profile'):
                request.session['Reg_Num'] = user.shopowner_profile.Reg_Num
                messages.success(request, "Login Success")
                return redirect('ShopHome')

        messages.error(request, "Invalid credentials")
        return redirect('LoginPage')
    return redirect('LoginPage')


def shop_signup(request):
    if request.method == 'POST':
        s_name = request.POST.get('sname')
        reg_num = request.POST.get('regnumber')
        s_mail = request.POST.get('smail')
        s_mobile = request.POST.get('smobile')
        s_pass = request.POST.get('spass')
        state = request.POST.get('state')
        dist = request.POST.get('dist')
        taluk = request.POST.get('taluk')
        panch = request.POST.get('panch')
        location = request.POST.get('place')

        if User.objects.filter(username=reg_num).exists():
            messages.error(request, "Registration Number already exists.")
            return redirect('Shop')

        try:
            # Create inactive user
            user = User.objects.create_user(username=reg_num, password=s_pass, email=s_mail, is_active=False)

            # Generate OTP and save to OTPVerification model
            otp = generate_otp()
            otp_expiry = now() + timedelta(minutes=10)  # OTP valid for 10 minutes
            OTPVerification.objects.create(user=user, otp=otp, otp_expiry=otp_expiry)

            # Send OTP via email
            send_otp_email(s_mail, otp)


            # Store details in session for later use
            request.session['shop_data'] = {
                's_name': s_name, 'reg_num': reg_num, 's_mail': s_mail, 's_mobile': s_mobile,
                'state': state, 'dist': dist, 'taluk': taluk, 'panch': panch, 'location': location
            }

            # Redirect to OTP verification page
            request.session['shop_email'] = s_mail
            return redirect('verify_shop_otp')

        except IntegrityError:
            messages.error(request, "Registration Number already exists.")
            return redirect('Shop')

    return redirect('Shop')

def verify_shop_otp(request):
    if request.method == "POST":
        email = request.session.get("shop_email")
        user = User.objects.filter(email=email).first()
        otp_entered = request.POST.get("otp")

        if not user:
            messages.error(request, "User not found.")
            return redirect("SignUpPage")

        otp_record = OTPVerification.objects.filter(user=user).first()

        if otp_record and otp_record.otp == otp_entered:
            if otp_record.is_valid():
                user.is_active = True  # Activate user after OTP verification
                user.save()

                # Retrieve shop data from session
                shop_data = request.session.get("shop_data", {})
                if shop_data:
                    ShopOwner.objects.create(
                        user=user,
                        S_Name=shop_data["s_name"],
                        Reg_Num=shop_data["reg_num"],
                        S_Mail=shop_data["s_mail"],
                        S_Mobile=shop_data["s_mobile"],
                        State=shop_data["state"],
                        District=shop_data["dist"],
                        Taluk=shop_data["taluk"],
                        Panchayat=shop_data["panch"],
                        Place=shop_data["location"]
                    )

                # Delete OTP record and session data
                otp_record.delete()
                del request.session["shop_email"]
                del request.session["shop_data"]

                messages.success(request, "Email verified successfully! You can now log in.")
                return redirect(login_page)

        messages.error(request, "Invalid or expired OTP. Try again.")
        return redirect("verify_shop_otp")

    return render(request, "verify_shop_otp.html")



def approve_request(request):
    return render(request, 'ApproveRequest.html')

def log_out(request):
    if request.session.get('Ration_Card'):
        request.session.pop('Ration_Card', None)
        request.session.pop('U_Pass', None)
        messages.info(request, "Logged Out Successfully")
    elif request.session.get('Reg_Num'):
        request.session.pop('Reg_Num', None)
        request.session.pop('S_Pass', None)
        messages.info(request, "Logged Out Successfully")
    elif request.session.get('delivery_partner'):
        request.session.pop('delivery_partner', None)
        request.session.pop('password', None)
        messages.info(request, "Logged Out Successfully")
    return redirect(login_page)


def contact_us(request):
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()
    shp = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    usr_name = request.session.get('Reg_Num') or request.session.get('Ration_Card')
    cart_count = CartDB.objects.filter(User_Name=usr_name, order__isnull=True)
    x = cart_count.count()
    return render(request, 'ContactUs.html', {'details': details, 'shp': shp, 'x': x})


def save_contact(request):
    if request.method == 'POST':
        n_ame = request.POST.get('FullName')
        e_mail = request.POST.get('Email')
        phn_num = request.POST.get('PhoneNumber')
        mess_age = request.POST.get('mesg')
        obj = ContactDB(F_Name=n_ame, C_Mail=e_mail, Phn_Num=phn_num, Mesg=mess_age)
        obj.save()
        messages.success(request, "Your Message Sent Successfully")
        return redirect(contact_us)


def about_page(request):
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()
    usr_name = request.session.get('Reg_Num') or request.session.get('Ration_Card')
    cart_count = CartDB.objects.filter(User_Name=usr_name, order__isnull=True)
    x = cart_count.count()
    shp = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    return render(request, 'AboutUs.html', {'details': details, 'shp': shp, 'x': x})


def single_product(request, si_id):
    # Get beneficiary details using Ration_Card from session
    ration_card = request.session.get('Ration_Card')
    prod = BeneficiaryRegister.objects.filter(Ration_Card=ration_card).first()

    # Fetch product details
    sing = RationItems.objects.get(id=si_id)

    # Check if the selected product is ATTA
    is_atta = sing.Ration.lower() == "atta"

    # Default atta quantity
    atta_quantity = 0

    # ATTA allocation based on card color
    if prod and is_atta:
        card_color = prod.Card_Color.lower()
        atta_allocations = {"yellow": 3, "pink": 2}
        atta_quantity = atta_allocations.get(card_color, 0)

    # Check if item is already in the cart (excluding ordered items)
    cart_item = CartDB.objects.filter(User_Name=ration_card, ration_item=sing, order__isnull=True).first()
    already_in_cart = bool(cart_item)

    # Family members count (default to 1 if not found)
    family_members = prod.Family_Members if prod and prod.Family_Members else 1

    # Quantity allocations by card color (excluding ATTA)
    card_allocations = {
        "yellow": {"White Rice": 9, "Boiled Rice": 15, "Raw Rice": 6, "Wheat": 5},
        "white": {"White Rice": 2, "Boiled Rice": 3, "Raw Rice": 1},
        "pink": {"White Rice": 1, "Boiled Rice": 2, "Raw Rice": 0.5, "Wheat": 0.5},
        "blue": {"White Rice": 0.5, "Boiled Rice": 1, "Raw Rice": 0.5},
    }

    # Calculate final quantity (skip ATTA)
    if prod and not is_atta:
        card_color = prod.Card_Color.lower()
        allocation = card_allocations.get(card_color, {})
        base_quantity = allocation.get(sing.Ration, 0)
        final_quantity = base_quantity if card_color in ["yellow", "white"] else base_quantity * family_members
    else:
        final_quantity = 0 if is_atta else 1 * family_members

    # Get active cart count
    cart_count = CartDB.objects.filter(User_Name=ration_card, order__isnull=True).count()

    return render(request, 'SingleProduct.html', {
        'sing': sing,
        'prod': prod,
        'final_quantity': final_quantity,
        'already_in_cart': already_in_cart,
        'details': prod,
        'x': cart_count,
        'atta_quantity': atta_quantity,
        'is_atta': is_atta
    })


def cart_page(request):
    user_identifier = request.session.get('Ration_Card') or request.session.get('Reg_Num')
    current_month = now().month
    current_year = now().year

    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()
    shp = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()

    if details:
        # Get all cart items not linked to an order
        crt = CartDB.objects.filter(User_Name=user_identifier, order__isnull=True)

        # Get items already ordered this month
        monthly_orders = OrderDB.objects.filter(
            User_Name=user_identifier,
            created_at__year=current_year,
            created_at__month=current_month
        )
        ordered_items = list(CartDB.objects.filter(order__in=monthly_orders).values_list('Item_Name', flat=True))

        # Remove already purchased items from the cart
        crt = crt.exclude(Item_Name__in=ordered_items)

    elif shp:
        crt = CartDB.objects.filter(User_Name=user_identifier, order__isnull=True)
        ordered_items = []  # No restrictions for shop owners
    else:
        crt = CartDB.objects.none()
        ordered_items = []

    total_price = crt.aggregate(Sum('I_Total'))['I_Total__sum'] or 0
    quant = sum(item.Item_Quantity for item in crt)
    item_count = crt.count()
    usr_name = user_identifier
    cart_count = CartDB.objects.filter(User_Name=usr_name, order__isnull=True)
    x = cart_count.count()

    return render(request, 'CartPage.html', {
        'crt': crt,
        'details': details,
        'shp': shp,
        'total_price': total_price,
        'item_count': item_count,
        'quant': quant,
        'x': x,
        'ordered_items': ordered_items,  # ✅ Pass purchased items to template
    })


def save_cart(request):
    print("DEBUG: save_cart view function is STARTING!")
    print(f"DEBUG: Request method: {request.method}")
    print(f"DEBUG: POST data received: {request.POST}")

    if request.method != 'POST':
        return redirect(shop_stock if request.session.get('Reg_Num') else products)

    user_identifier = request.session.get('Reg_Num') or request.session.get('Ration_Card')
    current_month = now().month
    current_year = now().year

    try:
        i_name = request.POST.get('rname', '').strip()
        i_quant = int(request.POST.get('rquant', 0))

        if request.session.get('Ration_Card'):  # If logged in using Ration Card
            i_price = float(request.POST.get('price', 0))
            i_total = float(request.POST.get('total', 0))
        else:  # If logged in using Reg_Num (Shop Owner)
            i_price = 0
            i_total = 0  # Price & Total are not needed
    except ValueError:
        print("DEBUG: Invalid data format received.")
        messages.error(request, "Invalid data received. Please try again.")
        return redirect(shop_stock if request.session.get('Reg_Num') else products)

    if i_quant <= 0:
        print("DEBUG: Invalid quantity.")
        messages.error(request, "Invalid quantity.")
        return redirect(shop_stock if request.session.get('Reg_Num') else products)

    if request.session.get('Ration_Card'):
        if i_price is None or i_total is None or i_price < 0:
            print("DEBUG: Invalid price or total.")
            messages.error(request, "Invalid price or total.")
            return redirect(products)

        try:
            ration_item = RationItems.objects.get(Ration=i_name)
        except RationItems.DoesNotExist:
            messages.error(request, "Item not found.")
            return redirect(products)

        if i_name != "ATTA":
            monthly_orders = OrderDB.objects.filter(
                User_Name=user_identifier,
                created_at__year=current_year,
                created_at__month=current_month
            )
            ordered_items = CartDB.objects.filter(order__in=monthly_orders).values_list('Item_Name', flat=True)

            if i_name in ordered_items:
                messages.error(request, "You have already purchased this item this month.")
                return redirect(products)

        CartDB.objects.create(
            User_Name=user_identifier,
            ration_item=ration_item,
            Item_Name=i_name,
            Item_Quantity=i_quant,
            I_Price=i_price,
            I_Total=i_total,
            Item_Image=ration_item.R_Image
        )
        messages.success(request, "Item added to cart.")

    else:  # Logged in as Shop Owner (Reg_Num)
        try:
            stock_item = Stock.objects.get(Item=i_name)
        except Stock.DoesNotExist:
            messages.error(request, "Stock item not found.")
            return redirect(shop_stock)

        CartDB.objects.create(
            User_Name=user_identifier,
            stock_item=stock_item,
            Item_Name=i_name,
            Item_Quantity=i_quant,
            I_Price=None,  # Not needed
            I_Total=i_total,  # Not needed
            Item_Image=stock_item.Item_Image
        )
        messages.success(request, "Item added to cart.")

    return redirect(shop_stock if request.session.get('Reg_Num') else products)


def delete_cart(request, crt_id):
    user_identifier = request.session.get('Ration_Card') or request.session.get('Reg_Num')  # Get user identifier

    del_cart = CartDB.objects.filter(
        id=crt_id,
        User_Name=user_identifier,  # Ensure it's the current user's cart item
        order__isnull=True  # <---- Crucial: Only delete if NOT associated with an order
    )
    messages.warning(request, "Deleted From Cart")

    if del_cart.exists():  # Check if the cart item to delete exists based on filters
        del_cart.delete()
        print(
            f"DEBUG: delete_cart - Cart item with ID {crt_id} deleted successfully from cart for user {user_identifier}.")  # Debug message
    else:
        print(
            f"DEBUG: delete_cart - Cart item with ID {crt_id} not found in user's cart or already part of an order. No deletion performed.")  # Debug message

    return redirect(cart_page)


def sin_up(request):
    return render(request, 'ShopSignUp.html')


def my_details(request, my_id):
    details = BeneficiaryRegister.objects.filter(id=my_id).first()
    det = ShopOwner.objects.filter(id=my_id).first()
    usr_name = request.session.get('Reg_Num') or request.session.get('Ration_Card')
    cart_count = CartDB.objects.filter(User_Name=usr_name, order__isnull=True)
    x = cart_count.count()
    return render(request, 'MyDetails.html', {'details': details, 'det': det, 'x': x})


def checkout_page(request):
    # Identify whether the user is a shop owner or a beneficiary
    shp_ownr = request.session.get('Reg_Num')
    usr_cust = request.session.get('Ration_Card')
    user_identifier = usr_cust or shp_ownr  # Pick whichever session value is set


    if shp_ownr:
        chk = CartDB.objects.filter(User_Name=shp_ownr, order__isnull=True)  # ADDED order__isnull=True (Correct)
    elif usr_cust:
        chk = CartDB.objects.filter(User_Name=usr_cust, order__isnull=True)  # ADDED order__isnull=True (Correct)
    else:
        chk = None

    # Calculate total_price based on *current cart items* (chk) - CORRECTED CALCULATION
    total_price = chk.aggregate(Sum('I_Total'))['I_Total__sum'] or 0
    item_count = chk.count()  # item_count should be based on *chk*

    # Fetch shop owner or beneficiary details for display
    shp = ShopOwner.objects.filter(Reg_Num=shp_ownr).first()
    details = BeneficiaryRegister.objects.filter(Ration_Card=usr_cust).first()
    usr_name = request.session.get('Reg_Num') or request.session.get('Ration_Card')
    cart_count = CartDB.objects.filter(User_Name=usr_name, order__isnull=True)
    x = cart_count.count()
    return render(request, 'CheckOut.html', {
        'chk': chk,  # Now 'chk' should only contain CURRENT cart items
        'details': details,
        'shp': shp,
        'total_price': total_price,  # Corrected total_price calculation
        'item_count': item_count,
        'x': x
    })


def shop_stock(request):
    details = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    stks = Stock.objects.all()
    usr_name = request.session.get('Reg_Num')
    cart_count = CartDB.objects.filter(User_Name=usr_name, order__isnull=True)
    x = cart_count.count()
    return render(request, 'ShopStock.html', {'details': details, 'stks': stks, 'x': x})


def shop_single_prod(request, s_id):
    details = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    singl = Stock.objects.get(id=s_id)
    produ = Stock.objects.all()
    usr_name = request.session.get('Reg_Num')
    cart_count = CartDB.objects.filter(User_Name=usr_name, order__isnull=True)
    x = cart_count.count()
    return render(request, 'ShopSingleProd.html', {'singl': singl, 'produ': produ, 'details': details, 'x': x})


def order_page(request):
    user_identifier = request.session.get('Ration_Card') or request.session.get('Reg_Num')

    if not user_identifier:
        print("DEBUG: order_page - No user_identifier found, redirecting to login.")
        return redirect('login')

    print(f"DEBUG: order_page - User identifier: {user_identifier}")

    orders = OrderDB.objects.filter(User_Name=user_identifier).prefetch_related(
        Prefetch('cart_items', queryset=CartDB.objects.all()),
        'status'  # Correct prefetch_related to 'status'
    )

    order_count = orders.count()
    print(f"DEBUG: order_page - Number of orders found: {order_count}")

    # *** UPDATED DEBUGGING LOOP - removed .count() from order.status ***
    print("DEBUG: order_page - Retrieved orders:")
    for order in orders:
        print(f"  - Order ID: {order.id}, Order Number: {order.Order_Num}, User: {order.User_Name}")
        print(f"    - Cart Items Count: {order.cart_items.count()}")
        if hasattr(order, 'status') and order.status:  # Check if order.status exists before accessing
            print(f"    - Order Status: {order.status.status}")  # Access single status object via order.status
        else:
            print("    - Order Status: No status set")
    # *** END of updated debugging loop ***

    total_price = sum(order.total for order in orders)
    shp = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()
    usr_name = request.session.get('Reg_Num') or request.session.get('Ration_Card')
    cart_count = CartDB.objects.filter(User_Name=usr_name, order__isnull=True)
    x = cart_count.count()
    return render(request, 'OrderPage.html', {
        'orders': orders,
        'total_price': total_price,
        'details': details,
        'shp': shp,
        'user': request.user,
        'x': x
    })



def save_checkout(request):
    if request.method != 'POST':
        return redirect('Home')

    user_identifier = request.session.get('Ration_Card') or request.session.get('Reg_Num')
    if not user_identifier:
        print("DEBUG: NO user_identifier found. Redirecting to login.")
        return redirect('login')

    # Get cart items for the user
    cart_items_for_order = CartDB.objects.filter(User_Name=user_identifier, order__isnull=True)
    if not cart_items_for_order.exists():
        print("DEBUG: Cart is EMPTY. Redirecting to CartPage.")
        return redirect('CartPage')

    shop_reg_num = None
    if request.session.get('Ration_Card'):
        beneficiary = BeneficiaryRegister.objects.filter(Ration_Card=request.session['Ration_Card']).first()
        if beneficiary:
            shop_reg_num = beneficiary.Shop_ID
    elif request.session.get('Reg_Num'):
        shop_reg_num = request.session['Reg_Num']

    shop_owner = ShopOwner.objects.filter(Reg_Num=shop_reg_num).first()
    if not shop_owner:
        first_cart_item = cart_items_for_order.first()
        if first_cart_item and first_cart_item.stock_item:
            shop_owner = first_cart_item.stock_item.Shop
            shop_reg_num = shop_owner.Reg_Num if shop_owner else None
    payment_method = request.POST.get('payment_method')
    if payment_method not in ['COD', 'Online']:
        payment_method = 'COD'
    amount = request.POST.get('amount')

    order = OrderDB.objects.create(
        Shop=shop_owner,
        User_Name=user_identifier,
        Name=request.POST.get('name'),
        Email=request.POST.get('email'),
        Address=request.POST.get('address'),
        Mobile=request.POST.get('mobile'),
        Card_Num=request.POST.get('cardnum', ''),
        payment_method=payment_method,
        amount=amount,
        Reg_Num=shop_reg_num
    )

    for cart_item in cart_items_for_order:
        cart_item.order = order
        cart_item.save()
    OrderStatus.objects.create(order=order, status='pending')
    cart_items_for_order.delete()

    if shop_owner and request.session.get('Reg_Num'):
        messages.success(request, "Stock Request Placed Successfully")  # Ensure it's a shop owner placing the order
        return redirect('ShopHome')

    if payment_method == 'COD':
        messages.success(request, "Order Placed Successfully")
        return redirect('Home')
    elif payment_method == 'Online':
        messages.success(request, "Order Placed Successfully")
        return redirect('PaymentPage')
    else:
        return redirect('ContactUs')




def delivery_partner(request):
    if not hasattr(request.user, 'delivery_profile'):
        print("DEBUG: User does not have a delivery profile.")
        return HttpResponse("You are not a delivery partner.")

    # Get the shop's registration number linked to the delivery partner
    shop_owner = ShopOwner.objects.filter(Reg_Num=request.user.delivery_profile.D_Shop.Reg_Num).first()
    shop_reg_num = shop_owner.Reg_Num if shop_owner else None

    # Exclude orders placed by shop owners
    shop_owner_reg_nums = ShopOwner.objects.values_list('Reg_Num', flat=True)
    orders = OrderDB.objects.filter(Reg_Num=shop_reg_num).exclude(User_Name__in=shop_owner_reg_nums).select_related(
        'Shop')

    # Count total delivered orders for the shop
    total_delivered = OrderStatus.objects.filter(status='delivered', order__Reg_Num=shop_reg_num).count()

    print(f"DEBUG: Displaying orders for shop Reg_Num={shop_reg_num}, excluding shop owner orders")

    return render(request, 'Delivery_Partner.html', {'orders': orders, 'total_delivered': total_delivered})



def signup_delivery(request):
    return render(request, 'DeliverySignUp.html')


def save_delivery_signup(request):
    if request.method == 'POST':
        dname = request.POST.get('d_name')
        shp_id = request.POST.get('shopid')
        pss = request.POST.get('passw')
        cpss = request.POST.get('cpassw')
        d_mbl = request.POST.get('mbl')
        # Use .get() to safely access the file from request.FILES
        pic = request.FILES.get('pic')

        if pss != cpss:
            messages.error(request, "Passwords do not match")
            return redirect('Delivery_SignUp')  # Assuming 'Delivery_SignUp' is your signup URL name

        try:
            shop = ShopOwner.objects.get(Reg_Num=shp_id)
        except ShopOwner.DoesNotExist:
            messages.error(request, "Invalid Shop Registration Number")
            return redirect('Delivery_SignUp')

        try:
            # 1. Create Django User object first (using username and password)
            user = User.objects.create_user(username=dname, password=pss)

            # 2. Then create Delivery profile linked to the User
            Delivery.objects.create(
                D_Partner=user,  # Link Delivery to the User object
                D_Shop=shop,
                D_Phone=d_mbl,
                D_Pic=pic
                # This now will be None if no file was uploaded, which is allowed if your model sets null=True, blank=True
            )
            messages.success(request, "Delivery Partner registration successful!")
            return redirect('PartnerDetails')

        except IntegrityError:
            messages.error(request, "Username already exists.")
            return redirect('Delivery_SignUp')

    return redirect('Delivery_SignUp')


RAZORPAY_KEY_ID = 'rzp_test_qtgRvY4PWS4ZIy'
RAZORPAY_SECRET_KEY = '2D7FeodPxKgqIiWZDYhkNc7L'


# Payment Page View
def payment_page(request):
    nm = OrderDB.objects.order_by('-id').first()

    if not nm:
        messages.error(request, "No active order found!")
        return redirect('CartPage')

    try:
        pay = nm.total  # Fetch total price
        amt = int(pay * 100)  # Convert to smallest currency unit (paisa)

        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET_KEY))
        payment = client.order.create({
            'amount': amt,
            'currency': 'INR',
            'payment_capture': 1  # Auto-capture payment
        })

        nm.razorpay_order_id = payment['id']
        nm.save()
        print("Razorpay payment object:", payment)

        return render(request, 'Payment.html', {
            'nm': nm,
            'pay_str': str(amt),
            'razorpay_order_id': payment['id'],
            'razorpay_key': RAZORPAY_KEY_ID
        })

    except Exception as e:
        messages.error(request, f"Payment error: {e}")
        return redirect('CartPage')


@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET_KEY))

            # Log received data for debugging
            print("Received data:", data)

            # Verify payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })

            # Update order status
            order = OrderDB.objects.get(razorpay_order_id=data['razorpay_order_id'])
            order.payment_status = "Paid"
            order.save()

            return JsonResponse({"success": True, "redirect_url": "/OrderPage"})

        except razorpay.errors.SignatureVerificationError as e:
            print("Signature verification failed:", e)
            return JsonResponse({"success": False, "error": "Invalid payment signature"})

        except OrderDB.DoesNotExist:
            print("Order not found for order ID:", data['razorpay_order_id'])
            return JsonResponse({"success": False, "error": "Order not found"})

        except Exception as e:
            print("Unexpected error:", e)
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})


def cancel_payment(request):
    messages.error(request, 'Payment Canceled')
    return redirect(checkout_page)

def request_page(request):
    # Get the current shop owner based on session Reg_Num
    reg_num = request.session.get('Reg_Num')
    shop_owner = ShopOwner.objects.filter(Reg_Num=reg_num).first()

    # Count items in the cart for the current shop owner
    cart_count = CartDB.objects.filter(User_Name=reg_num, order__isnull=True).count()

    # Get all orders linked to the shop owner's Reg_Num
    shop_orders = OrderDB.objects.filter(Reg_Num=reg_num)

    # Filter orders placed by beneficiaries (users in BeneficiaryRegister)
    beneficiary_orders = shop_orders.filter(
        User_Name__in=BeneficiaryRegister.objects.values_list('Ration_Card', flat=True)
    )

    return render(request, 'Request.html', {
        'shp': shop_owner,
        'x': cart_count,
        'order_n': beneficiary_orders,
    })


def update_status(request, order_num):
    if request.method == 'POST':
        new_status = request.POST.get('status')  # Get the new status from the form data
        order = get_object_or_404(OrderDB, Order_Num=order_num)  # Get the order using Order_Num
        order_status = order.status  # Access the related OrderStatus

        order_status.status = new_status  # Update the status
        order_status.save()
        messages.success(request, "Status Updated")
    # Redirect based on the user's role. Shop owners are taken back to their Requests page.
    if request.session.get('Reg_Num'):
        return redirect('Requests')  # Change 'Requests' to your shop owner-specific URL name if needed
    else:
        return redirect('Delivery_Partner')


def order_details(request, order_num):
    order = get_object_or_404(OrderDB, Order_Num=order_num)  # Fetch the order by order_num
    print(f"Order Amount: {order.amount}, Payment Method: {order.payment_method}")
    cart_items = order.cart_items.all()  # Get related cart items for this order
    order_status = order.status  # Get the associated order status
    shp = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()
    all_orders = OrderDB.objects.all()
    usr_name = request.session.get('Reg_Num')
    cart_count = CartDB.objects.filter(User_Name=usr_name, order__isnull=True)
    x = cart_count.count()
    order_n = []

    for order in all_orders:
        if BeneficiaryRegister.objects.filter(Ration_Card=order.User_Name).exists():
            order_n.append(order)
    context = {
        'order': order,
        'cart_items': cart_items,
        'order_status': order_status,
        'details': details,
        'shp': shp,
        'order_n': order_n,
        'x': x

    }

    # Use a different template or add extra context for shop owners if needed
    return render(request, 'OrderStatus.html', context)


def delivery_partner_list(request):
    if hasattr(request.user, 'shopowner_profile'):
        shopowner = request.user.shopowner_profile
        partners = Delivery.objects.filter(D_Shop=shopowner)
        return render(request, 'DeliveryPartnerDetails.html', {'partners': partners})
    else:
        messages.error(request, "Only shop owners can view delivery partners.")
        return redirect('ShopHome')


def forgot_password(request):
    if request.method == "POST":
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            request.session['reset_username'] = username  # Store username for reset
            return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, "Username not found.")
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')


def reset_password(request):
    if request.method == "POST":
        username = request.session.get('reset_username')  # Get username from session
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)  # Hashes and saves password
            user.save()

            # Clear session and show success message
            del request.session['reset_username']
            messages.success(request, "Password reset successful! Please log in.")
            return redirect('LoginPage')
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('forgot_password')

    return render(request, 'reset_password.html')
