
# RationKart

RationKart is a Django-based platform designed to digitize and optimize ration distribution workflows for Shop Owners, Beneficiaries, Delivery Partners, and Administrators. By leveraging modern web technologies, RationKart aims to enhance the efficiency and transparency of ration management systems.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Features

- **Role-Based Access:** Custom dashboards tailored for Shop Owners, Beneficiaries, Delivery Partners, and Admins.
- **Secure Authentication:** OTP verification via the SendGrid API ensures authorized access.
- **Scalable Database:** Transitioned from SQLite (for local development) to PostgreSQL (in production on Render) to efficiently manage users and complex queries.
- **Responsive Design:** User interface crafted with HTML, CSS, and JavaScript for optimal user experience.

## Tech Stack

- **Backend:** Django
- **Database:** PostgreSQL (deployed on Render), SQLite( Local Deployment )
- **Deployment:** Render using Gunicorn and WhiteNoise
- **Security:** Implemented session management, encrypted OTP workflows, and role-based permissions.

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

5. **Install the required dependencies:**

   
   pip install -r requirements.txt
  

6. **Set up the database:**

   - Apply migrations:
     python manage.py makemigrations
     python manage.py migrate

7. **Run the development server:**

   python manage.py runserver

   The application will be accessible at `http://127.0.0.1:8000/`.

## Usage

1. **Access the application:**

   Open your web browser and navigate to `http://127.0.0.1:8000/`.

2. **User Registration:**
   - Users have to register as a shop owner first, as the beneficiary has to be approved by the shopowner to complete registration.
   - The Shopowner can approve a beneficiary after logging in, by going to "My Profile" in the user icon and then clicking the "Approve           Requests" button 
   - Users can register based on their roles: Shop Owner, Beneficiary, or Delivery Partner.
   - During ShopOwner registration, an OTP will be sent via email for verification. So, ensure to give a valid E-Mail ID.

3. **Dashboard Access:**

   - Upon successful login, users will be redirected to their respective dashboards tailored to their roles.

4. **Manage Ration Distribution:**

   - Shop Owners can manage orders, view delivery logs, and also able to sign up Delivery Partners.
   - Shop Owners can request more stock from the Admin.
   - Beneficiaries can view their ration entitlements and history.
   - Delivery Partners can view delivery schedules and confirm deliveries.
   - Admins can oversee the entire system, manage users, and generate reports.

## License

This project is licensed under the [MIT License](LICENSE).


We invite you to explore the project and share your thoughts. Your feedback is highly appreciated.
```
