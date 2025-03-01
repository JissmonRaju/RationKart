from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db.models import Sum
from django.db.models import Prefetch
from AdminApp.models import Stock, RationItems
from WebApp.models import BeneficiaryRegister, ContactDB, CartDB, ShopOwner, OrderDB, OrderStatus, Delivery
from django.contrib import messages
from django.db import IntegrityError
import AdminApp.models
import razorpay


# Create your views here.

def home(request):

    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()
    cart_count = CartDB.objects.filter(User_Name=request.session['Ration_Card'],order__isnull=True)
    x = cart_count.count()
    stks = Stock.objects.all()
    return render(request, 'Home.html', {'stks': stks, 'details': details,'x':x})


def products(request):
    cart_count = CartDB.objects.filter(User_Name=request.session['Ration_Card'],order__isnull=True)
    x = cart_count.count()
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()

    prod = RationItems.objects.all()
    return render(request, 'Products.html', {'prod': prod, 'details': details,'x':x})


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

        try:
            # 1. Create Django User object, set username to Ration_Card
            user = User.objects.create_user(username=ration_card, password=u_pass)  # Use ration_card as username

            # 2. Create BeneficiaryRegister profile, linked to the User
            beneficiary = BeneficiaryRegister.objects.create(
                user=user,  # Link to the User object
                U_Name=u_name,
                Ration_Card=ration_card,  # Store Ration_Card in profile as well
                Card_Color=card_color,
                U_Mail=u_mail,
                U_Mobile=u_mobile,
                Family_Members=fam_members
            )
            messages.success(request, "Registration successful! Please login")
            return redirect('LoginPage')  # Redirect to login page

        except IntegrityError:  # Catch username (Ration_Card) already exists error
            messages.error(request, "Ration Card number already exists")
            return redirect('SignUpPage')  # Redirect back to signup page (update template name if needed)

    return redirect('SignUpPage')


def shop_signup(request):
    if request.method == 'POST':
        s_name = request.POST.get('sname')
        reg_num = request.POST.get('regnumber')
        s_mail = request.POST.get('smail')
        s_mobile = request.POST.get('smobile')
        s_pass = request.POST.get('spass')

        try:
            # 1. Create Django User object, set username to Reg_Num
            user = User.objects.create_user(username=reg_num, password=s_pass)  # Use reg_num as username

            # 2. Create ShopOwner profile, linked to the User
            shop_owner = ShopOwner.objects.create(
                user=user,  # Link to User object
                S_Name=s_name,
                Reg_Num=reg_num,  # Store Reg_Num in profile as well
                S_Mail=s_mail,
                S_Mobile=s_mobile,
            )
            messages.success(request, "Shop Owner registration successful! Please login.")
            return redirect('LoginPage')  # Redirect to login page

        except IntegrityError:  # Catch username (Reg_Num) already exists error
            messages.error(request, "Registration Number already exists.")
            return redirect('ShopSignUpPage')  # Redirect back to signup page (update template name if needed)

    return redirect('ShopSignUpPage')


def shop_home(request):
    det = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    cart_count = CartDB.objects.filter(User_Name=request.session['Reg_Num'],order__isnull=True)
    x = cart_count.count()
    return render(request, 'ShopHome.html', {'det': det,'x':x})


def login_page(request):
    return render(request, 'LoginPage.html')


def save_login(request):
    if request.method == 'POST':
        uname_e = request.POST.get('uname')
        pass_words = request.POST.get('pass')
        user = authenticate(username=uname_e, password=pass_words)  # Authenticate using Django auth

        if user is not None:  # Authentication successful
            login(request, user)  # Use Django's login

            # Clear session data (Session Isolation)
            request.session.pop('Reg_Num', None)
            request.session.pop('delivery_partner', None)
            request.session.pop('Ration_Card', None)

            if user.is_superuser:
                return redirect('Index')  # Superuser

            if hasattr(user, 'delivery_profile'):  # Check for Delivery Partner profile
                request.session['delivery_partner'] = user.username
                return redirect('Delivery_Partner')

            if hasattr(user, 'beneficiary_profile'):  # Check for Beneficiary profile
                beneficiary = user.beneficiary_profile  # Access BeneficiaryRegister via related_name
                request.session['Ration_Card'] = beneficiary.Ration_Card  # Store Ration_Card from related profile
                return redirect('Home')

            if hasattr(user, 'shopowner_profile'):  # Check for ShopOwner profile
                shopowner = user.shopowner_profile  # Access ShopOwner via related_name
                request.session['Reg_Num'] = shopowner.Reg_Num  # Store Reg_Num from related profile
                return redirect(reverse('ShopHome'))

        messages.error(request, "Invalid credentials")  # Error message for failed login
        return redirect('LoginPage')  # Redirect to login page

    return redirect('LoginPage')


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
    usr_name = request.session.get('Reg_Num') or request.session.get('Ration_Card')
    cart_count = CartDB.objects.filter(User_Name=usr_name,order__isnull=True)
    x = cart_count.count()
    return render(request, 'ContactUs.html', {'details': details, 'shp': shp,'x':x})


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
    usr_name = request.session.get('Reg_Num') or request.session.get('Ration_Card')
    cart_count = CartDB.objects.filter(User_Name=usr_name,order__isnull=True)
    x = cart_count.count()
    shp = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    return render(request, 'AboutUs.html', {'details': details, 'shp': shp,'x':x})


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

    usr_name = request.session.get('Ration_Cart')
    cart_count = CartDB.objects.filter(User_Name=usr_name,order__isnull=True)
    x = cart_count.count()
    return render(request, 'SingleProduct.html', {
        'sing': sing,
        'prod': prod,
        'final_quantity': final_quantity,
        'already_in_cart': already_in_cart,
        'details': details,
        'x':x
    })


def cart_page(request):
    details = BeneficiaryRegister.objects.filter(Ration_Card=request.session.get('Ration_Card')).first()
    shp = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
  # Get user identifier

    if details:
        crt = CartDB.objects.filter(User_Name=request.session['Ration_Card'],
                                    order__isnull=True)  # UPDATED - added order__isnull=True
    elif shp:
        crt = CartDB.objects.filter(User_Name=request.session['Reg_Num'],
                                    order__isnull=True)  # UPDATED - added order__isnull=True
    else:
        crt = None

    # Calculate total_price based on *current cart items* (crt) - CORRECTED CALCULATION
    total_price = crt.aggregate(Sum('I_Total'))['I_Total__sum'] or 0
    quant = 0
    for i in crt:  # Iterate over *crt*, not the unfiltered 'ord'
        quant += i.Item_Quantity

    item_count = crt.count()  # item_count should also be based on *crt*
    usr_name = request.session.get('Reg_Num') or request.session.get('Ration_Card')
    cart_count = CartDB.objects.filter(User_Name=usr_name,order__isnull=True)
    x = cart_count.count()
    return render(request, 'CartPage.html',
                  {'crt': crt, 'details': details, 'shp': shp, 'total_price': total_price, 'item_count': item_count,
                   'quant': quant,'x':x})


def save_cart(request):
    print("DEBUG: save_cart view function is STARTING!")  # Function start debug
    print(f"DEBUG: Request method: {request.method}")  # Print request method

    if request.method == 'POST':
        print("DEBUG: Request is POST, proceeding to process cart item...")  # POST request confirmed

        print("DEBUG: request.POST data:")  # Print the entire request.POST dictionary
        for key, value in request.POST.items():
            print(f"  - {key}: {value}")

        user_identifier = request.session.get('Reg_Num') or request.session.get('Ration_Card')
        if request.session.get('Reg_Num'):  # Shop Owner is adding to cart
            i_name = request.POST.get('rname')
            usr_name = request.session.get('Reg_Num')
            i_price = request.POST.get('rprice')
            i_quant = request.POST.get('rquant')
            i_total = request.POST.get('rtotal')
            img = None

            try:
                stock_item_obj = AdminApp.models.Stock.objects.get(Item=i_name)
                img = stock_item_obj.Item_Image
            except AdminApp.models.Stock.DoesNotExist:
                pass

            obj = CartDB(
                User_Name=usr_name,
                stock_item=stock_item_obj,
                Item_Name=i_name,
                Item_Quantity=int(i_quant),
                I_Price=i_price,
                I_Total=i_total,
                Item_Image=img,
            )
            obj.save()
            print(
                f"DEBUG: CartDB object SAVED for Shop Owner. Item Name: {i_name}, Quantity: {i_quant}")  # CartDB save debug - Shop Owner

        elif request.session.get('Ration_Card'):  # Beneficiary is adding to cart
            i_name = request.POST.get('iname')
            usr_name = request.session.get('Ration_Card')
            i_price = request.POST.get('price')
            i_quant = request.POST.get('quant')
            i_total = request.POST.get('total')
            img = None

            try:
                ration_item_obj = AdminApp.models.RationItems.objects.get(Ration=i_name)
                img = ration_item_obj.R_Image
            except AdminApp.models.RationItems.DoesNotExist:
                pass

            obj = CartDB(
                User_Name=usr_name,
                ration_item=ration_item_obj,
                Item_Name=i_name,
                Item_Quantity=int(i_quant),
                I_Price=i_price,
                I_Total=i_total,
                Item_Image=img,
            )
            obj.save()
            print(
                f"DEBUG: CartDB object SAVED for Beneficiary. Item Name: {i_name}, Quantity: {i_quant}")  # CartDB save debug - Beneficiary
        else:
            print(
                "DEBUG: No user session (Reg_Num or Ration_Card).  This should not happen in POST request.")  # User session missing debug - should not happen in POST

        if request.session.get('Reg_Num'):
            return redirect(shop_stock)
        elif request.session.get('Ration_Card'):
            return redirect(products)
    else:
        print("DEBUG: Request is NOT POST. Redirecting based on user session...")  # Non-POST redirect debug
        if request.session.get('Reg_Num'):
            return redirect(shop_stock)  # Redirect Shop Owner on non-POST
        elif request.session.get('Ration_Card'):
            return redirect(products)  # Redirect Beneficiary on non-POST
        else:
            print(
                "DEBUG: No user session in non-POST request. Redirecting to Home.")  # No user session debug - non-POST
            return redirect(home)  # Default redirect to home if no session in non-POST


def delete_cart(request, crt_id):
    user_identifier = request.session.get('Ration_Card') or request.session.get('Reg_Num')  # Get user identifier

    del_cart = CartDB.objects.filter(
        id=crt_id,
        User_Name=user_identifier,  # Ensure it's the current user's cart item
        order__isnull=True  # <---- Crucial: Only delete if NOT associated with an order
    )

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
    cart_count = CartDB.objects.filter(User_Name=usr_name,order__isnull=True)
    x = cart_count.count()
    return render(request, 'MyDetails.html', {'details': details, 'det': det,'x':x})


def checkout_page(request):
    # Identify whether the user is a shop owner or a beneficiary
    shp_ownr = request.session.get('Reg_Num')
    usr_cust = request.session.get('Ration_Card')
    user_identifier = usr_cust or shp_ownr  # Pick whichever session value is set

    # Determine which cart items to pass as 'chk' - CORRECTED QUERY (already done previously)
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
    cart_count = CartDB.objects.filter(User_Name=usr_name,order__isnull=True)
    x = cart_count.count()
    return render(request, 'CheckOut.html', {
        'chk': chk,  # Now 'chk' should only contain CURRENT cart items
        'details': details,
        'shp': shp,
        'total_price': total_price,  # Corrected total_price calculation
        'item_count': item_count,
        'x':x
    })


def shop_stock(request):
    details = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    stks = Stock.objects.all()
    usr_name = request.session.get('Reg_Num')
    cart_count = CartDB.objects.filter(User_Name=usr_name,order__isnull=True)
    x = cart_count.count()
    return render(request, 'ShopStock.html', {'details': details, 'stks': stks,'x':x})


def shop_single_prod(request, s_id):
    details = ShopOwner.objects.filter(Reg_Num=request.session.get('Reg_Num')).first()
    singl = Stock.objects.get(id=s_id)
    produ = Stock.objects.all()
    usr_name = request.session.get('Reg_Num')
    cart_count = CartDB.objects.filter(User_Name=usr_name,order__isnull=True)
    x = cart_count.count()
    return render(request, 'ShopSingleProd.html', {'singl': singl, 'produ': produ, 'details': details,'x':x})




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
    cart_count = CartDB.objects.filter(User_Name=usr_name,order__isnull=True)
    x = cart_count.count()
    return render(request, 'OrderPage.html', {
        'orders': orders,
        'total_price': total_price,
        'details': details,
        'shp': shp,
        'user': request.user,
        'x':x
    })


def save_checkout(request):
    print("DEBUG: save_checkout view function is STARTING!")

    if request.method == 'POST':
        user_identifier = request.session.get('Ration_Card') or request.session.get('Reg_Num')

        if not user_identifier:
            print("DEBUG: NO user_identifier found. Redirecting to login.")
            return redirect('login')

        cart_items_for_order = CartDB.objects.filter(User_Name=user_identifier, order__isnull=True)

        if not cart_items_for_order.exists():
            print("DEBUG: Cart is EMPTY. Redirecting to CartPage.")
            return redirect('CartPage')

        first_cart_item = cart_items_for_order.first()
        shop_owner = None
        if first_cart_item and first_cart_item.stock_item:
            shop_owner = first_cart_item.stock_item.Shop
            print(f"DEBUG: ShopOwner determined: {shop_owner}")

        order = OrderDB.objects.create(
            Shop=shop_owner,
            User_Name=user_identifier,
            Name=request.POST.get('name'),
            Email=request.POST.get('email'),
            Address=request.POST.get('address'),
            Mobile=request.POST.get('mobile'),
            Card_Num=request.POST.get('cardnum', ''),
            Reg_Num=request.POST.get('regnum', '')
        )
        order_id = order.id
        print(f"DEBUG: Order CREATED. Order ID: {order_id}, Order Number: {order.Order_Num}")

        for cart_item in cart_items_for_order:
            cart_item.order = order
            cart_item.save()

        OrderStatus.objects.create(order=order, status='pending')
        print(f"DEBUG: OrderStatus CREATED for Order ID: {order_id}")

        cart_items_to_clear = CartDB.objects.filter(User_Name=user_identifier, order__isnull=True)
        if cart_items_to_clear.exists():
            cart_items_to_clear.delete()
            print(f"DEBUG: save_checkout - Cart CLEARED for user {user_identifier} after checkout.")
        else:
            print(f"DEBUG: save_checkout - Cart was already empty for user {user_identifier}.")

        # Corrected conditional check using .get() with a default of None
        if request.session.get('Ration_Card') is not None:  # Use .get() to avoid KeyError
            print("DEBUG: Beneficiary checkout - Redirecting...")
            # Define 'home' and 'payment_page' URLs - replace placeholders with your actual URL names
            home_url = 'Home'  # Replace 'Home' with your actual URL name for beneficiary home
            payment_page_url = 'payment_page'  # Replace 'payment_page' with your payment URL
            return redirect(home_url) if request.POST.get('payment_option') == 'cod' else redirect(payment_page_url)
        elif request.session.get('Reg_Num') is not None:  # Use .get() for Reg_Num too
            print("DEBUG: Shop Owner checkout - Redirecting to shop home...")  # Debug for shop owner path
            shop_home_url = 'ShopHome'  # Replace 'ShopHome' with actual shop home URL
            return redirect(shop_home_url)
        else:
            print(
                "DEBUG: No user type identified in session during checkout. This should not happen under normal circumstances. Redirecting to Home.")  # Critical error debug
            return redirect('Home')  # Fallback redirect - consider redirecting to login page instead

    print("DEBUG: Request method is NOT POST. Redirecting to Home.")
    return redirect('Home')


def delivery_partner(request):
    all_orders = OrderDB.objects.all()
    beneficiary_orders = []
    for order in all_orders:
        if BeneficiaryRegister.objects.filter(Ration_Card=order.User_Name).exists():
            beneficiary_orders.append(order)

    return render(request, 'Delivery_Partner.html', {'order_n': beneficiary_orders})


def update_status(request, order_num):
    if request.method == 'POST':
        new_status = request.POST.get('status')  # Get the new status from the form data

        order = get_object_or_404(OrderDB, Order_Num=order_num)  # Get the OrderDB instance using Order_Num
        order_status = order.status  # Access the related OrderStatus

        order_status.status = new_status  # Update the status
        order_status.save()  # Save the updated OrderStatus

    return redirect('Delivery_Partner')


def order_details(request, order_num):  # 1. Accept order_num as URL parameter
    order = get_object_or_404(OrderDB, Order_Num=order_num)  # 2. Fetch SINGLE order by order_num
    cart_items = order.cart_items.all()  # 3. Get related cart items for this order
    order_status = order.status  # 4. Get related order status

    context = {
        'order': order,  # Pass the single order object
        'cart_items': cart_items,  # Pass the cart items related to this order
        'order_status': order_status,  # Pass the order status object
    }
    return render(request, 'OrderStatus.html', context)  # Render with context


def signup_delivery(request):
    return render(request, 'DeliverySignUp.html')


def save_delivery_signup(request):
    if request.method == 'POST':
        dname = request.POST.get('d_name')
        shp_id = request.POST.get('shopid')
        pss = request.POST.get('passw')
        cpss = request.POST.get('cpassw')
        d_mbl = request.POST.get('mbl')

        if pss != cpss:
            messages.error(request, "Passwords do not match")
            return redirect(signup_delivery)  # Assuming 'signup_delivery' is your signup URL name

        try:
            shop = ShopOwner.objects.get(Reg_Num=shp_id)
        except ShopOwner.DoesNotExist:
            messages.error(request, "Invalid Shop Registration Number")
            return redirect(signup_delivery)

        try:
            # 1. Create Django User object FIRST (using username and password)
            user = User.objects.create_user(username=dname, password=pss)

            # 2. Then create Delivery profile linked to the User
            Delivery.objects.create(
                D_Partner=user,  # Link Delivery to the User object
                D_Shop=shop,
                D_Phone=d_mbl
            )
            messages.success(request, "Delivery Partner registration successful! Please login.")
            return redirect('LoginPage')  # Redirect to login page

        except IntegrityError:  # Catch username already exists error (from User model)
            messages.error(request, "Username already exists.")
            return redirect(signup_delivery)

    return redirect(signup_delivery)


def payment_page(request):
    nm = OrderDB.objects.order_by('-id').first()

    pay = nm.total  # fetching total price

    amt = int(pay * 100)  # converting to smallest currency unit (paisa)

    pay_str = str(amt)  # reconverting to string

    if request.method == 'POST':
        ord_currency = 'INR'
        client = razorpay.Client(auth=('2D7FeodPxKgqIiWZDYhkNc7L', 'rzp_test_qtgRvY4PWS4ZIy'))
        payment = client.order.create({'amount': amt, 'currency': ord_currency})

    return render(request, 'Payment.html', {'nm': nm, 'pay_str': pay_str})


def cancel_payment(request):
    messages.error(request, 'Payment Canceled')
    return redirect(checkout_page)
