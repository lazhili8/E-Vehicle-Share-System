# E-Vehicle-Share-System
E-Vehicle Share System
CHIME E-Vehicle Sharing System 

![image](https://github.com/user-attachments/assets/7d739f2a-b8a5-45f5-8d96-04bb46efa754)
![image](https://github.com/user-attachments/assets/1e511943-914c-4152-b4ef-a85f4fb7a2d3)
![image](https://github.com/user-attachments/assets/bec0f619-1350-4269-a144-51fe5052982a)
![image](https://github.com/user-attachments/assets/90f62db8-0f50-46f3-8918-c65dac2ccbcf)
![image](https://github.com/user-attachments/assets/7048b2f1-8f76-4fc4-bdcf-4bf9281e559b)
![image](https://github.com/user-attachments/assets/3ecde0ae-8478-455d-8ff1-295a439c1150)
![image](https://github.com/user-attachments/assets/35553271-7cda-47fc-ba24-4c4f6b6d538c)
![image](https://github.com/user-attachments/assets/d2f23bfe-8cf3-460e-95c6-a1e7a3edb319)
![image](https://github.com/user-attachments/assets/4a374347-95c2-42fd-9963-5e6ddc2452c6)
![image](https://github.com/user-attachments/assets/ed6d1c8a-ad68-4593-bf5c-823279a17002)
![image](https://github.com/user-attachments/assets/bcb9313e-85f5-4d35-b4c7-63cb6dfebc97)



Overview

The CHIME E-Vehicle Sharing System is a web-based application designed to facilitate the rental of electric vehicles, specifically e-bikes and e-scooters. Built using the Django framework, this system aims to provide a convenient and eco-friendly solution for urban transportation, addressing the challenges of traffic congestion and environmental sustainability.

Features:

User Management: Secure registration and login for customers, operators, and managers.

Vehicle Availability: Real-time tracking of e-bike and e-scooter availability at various locations.

Rental Process: Seamless rental process including vehicle selection, booking, and payment processing.

Payment Integration: Basic payment processing with a history of transactions.

Operator Functionality: Operators can charge, move, and track vehicles.

Manager Functionalities: Managers can generate reports and visualize customer data for operational insights.

Technologies Used

Backend: Django, Django REST Framework

Frontend: HTML, CSS (Tailwind CSS), JavaScript

Database: SQLite (with the option to scale to PostgreSQL or MySQL)

APIs: Google Maps API for location services

INSTALLATION

Prerequisites : Python 3.x Django 3.x or later pip (Python package installer)

Steps to Install:

Copy code python -m venv venv source venv/bin/activate # On Windows use venv\Scripts\activate

Install Requirements: pip install -r requirements.txt

pip install django

pip install django-cors-headers
pip install django-cors-headers djangorestframework

pip install djangores

Set Up the Database: Run the following commands to set up the database:

python manage.py migrate **Create a Superuser (for admin access):

username:

emailaddress

password:

python manage.py createsuperuser

Run the Development Server:

python manage.py runserver

Access the Application:

Open your web browser and go to http://127.0.0.1:8000/.

Configuration : Update the settings.py file to configure the database settings, allowed hosts, and other environment-specific settings.

After opening. http://127.0.0.1:8000/.

User Registration: Users can sign up and create an account.

sample id
customer, operator, manager
email id : kaizhi@gmail.com
password: kaizhi


Finding Available Vehicles: Users can search for and find nearby e-bikes and e-scooters.

Rental Process: Users can book vehicles, return them, and manage their rental history.

Operator and Manager Functions: Operators can manage vehicle conditions, while managers can generate reports and monitor system performance.
