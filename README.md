
# RationKart

RationKart is a Django-based platform designed to digitize and optimize ration distribution workflows for Shop Owners, Beneficiaries, Delivery Partners, and Administrators. By leveraging modern web technologies, RationKart enhances the efficiency and transparency of ration management systems.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Features

- **Role-Based Access:** Custom dashboards for Shop Owners, Beneficiaries, Delivery Partners, and Admins.
- **Secure Authentication:** OTP verification via SendGrid API for authorized access.
- **Payment Integration:** Secure payment processing via Razorpay API for seamless transactions and payment history tracking.
- **Scalable Database:** Uses PostgreSQL in production (deployed on Render) and SQLite for local development.
- **Responsive Design:** User interface built with HTML, CSS, and JavaScript for seamless cross-device compatibility.

## Tech Stack

- **Backend:** Django
- **Database:** PostgreSQL (Production), SQLite (Local Development)
- **Deployment:** Render (Gunicorn + WhiteNoise)
- **APIs & Services:** SendGrid (OTP), Razorpay (Payments)
- **Security:** Session management, encrypted OTP workflows, and role-based permissions.


## Installation

To set up the project locally:

1. **Clone the repository:**
  
   git clone https://github.com/JissmonRaju/RationKart.git
  

2. **Navigate to the project directory:**
 
   cd RationKart
   

3. **Create a virtual environment:**
  
   python -m venv env


4. **Activate the virtual environment:**

     env\Scripts\activate

5. **Install dependencies:**
   
   pip install -r requirements.txt

6. **Environment Configuration:**

    -Create a .env file in your project root with the following variables:
   
    #**Django Settings**
   
    SECRET_KEY=your_django_secret_key_here  # Generate using: `python -c 'from django.core.management.utils import get_random_secret_key;    print(get_random_secret_key())'`
   
    DEBUG=True                             # Set to False in production
   
    ALLOWED_HOSTS=localhost,127.0.0.1     # Add production domain in live deployment
   
    CSRF_TRUSTED_ORIGINS=http://localhost:8000,https://your-published-domain
    
    #**Database (Development)**
   
    DATABASE_URL=sqlite:///db.sqlite3
    
   #**Database (Production - Render PostgreSQL)**
     #DATABASE_URL=postgresql://[USER]:[PASSWORD]@[HOST]/[DB_NAME]
    
    #**SendGrid (OTP)**
   
    SENDGRID_API_KEY=your_sendgrid_api_key_here
    DEFAULT_FROM_EMAIL=your_email@domain.com
    SENDGRID_SANDBOX_MODE_IN_DEBUG=False
    
   #**Razorpay (Payments)**
   
    RAZORPAY_KEY_ID=your_razorpay_key_id
    RAZORPAY_KEY_SECRET=your_razorpay_key_secret

8. **Set up the database:**
   - Apply migrations:
     
     python manage.py makemigrations
     python manage.py migrate
     

9. **Run the development server:**
  
   python manage.py runserver
  
   Access the application at `http://127.0.0.1:8000/`.

## Usage

1. **Access the application:**
   Navigate to `http://127.0.0.1:8000/` in your web browser.

2. **User Registration:**
   - **Shop Owners:** Register first, as beneficiaries require shop owner approval.
   - **Beneficiaries:** Submit registration requests via Shop Owners.
   - **OTP Verification:** Shop Owners receive an OTP via email during registration (ensure a valid email).

3. **Approval Workflow:**
   - Shop Owners approve beneficiaries via "My Profile" → "Approve Requests".

4. **Dashboard Features:**
   - **Shop Owners:**
     - Manage orders and delivery logs
     - Request stock replenishment from Admins
     - Register Delivery Partners
   - **Beneficiaries:** View ration entitlements, order rations and view orders
   - **Delivery Partners:** Track and confirm deliveries
   - **Admins:** Oversee system operations and generate reports


## License

Licensed under the [MIT License](LICENSE.md).

---

**We welcome your feedback and suggestions!** 💬

