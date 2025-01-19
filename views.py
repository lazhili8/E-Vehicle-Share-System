import random
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Rental, Payment,Vehicle
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Rental, Payment
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Location
import json
from django.utils.dateparse import parse_date
# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vehicle
from .serializers import VehicleSerializer
from .models import Rental, Vehicle, Payment, Operator, Manager, Customer




User = get_user_model()


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def bill(request):
    return render(request, 'bill.html')



def user_messages(request):
    return render(request, 'messages.html')

def vehicle(request):
    return render(request, 'vehicle.html')

def map(request):
    return render(request,'map.html')

def moving(request):
    return render(request,'moving.html')
def charge(request):
    return render(request,'charge_vehicle.html')

def e_scooter(request):
    return render(request, 'E-Scooter.html')

def e_bike(request):
    return render(request, 'E-Bike.html')

def manager_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('manager_home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('manager_login')

    return render(request, 'manager_login.html')


def manager_home_view(request):
    return render(request, 'manager.html')


def operator_home_view(request):
    return render(request, 'operator.html')

def operator_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('operator_home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('operator_login')

    return render(request, 'operator_login.html')


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')


        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')


        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')


        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()

        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')

    return render(request, 'register.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            unpaid_rental = Rental.objects.filter(customer=user, endTime__isnull=False, payment__is_paid=False).first()
            if unpaid_rental:
                return redirect('pay', rental_id=unpaid_rental.rentalID)

            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')

    return render(request, 'login.html')




def logout_view(request):
    logout(request)
    return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = get_random_string(20)

            reset_link = f"http://127.0.0.1:8000/"
            send_mail(
                'Password Reset Request',
                f'You requested a password reset. Click the link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'We have sent you an email with instructions to reset your password.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
        return redirect('reset_password')
    return render(request, 'reset_password.html')

def reset_confirm(request, token):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        try:
            user = User.objects.get(token=token)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid token.')
    return render(request, 'reset_confirm.html')

def return1(request):
    return render(request, 'return1.html')
def moving(request):
    return render(request, 'moving.html')

import threading
import time
active_threads = {}

def update_vehicle_status(rental):
    vehicle = rental.vehicle
    battery_drain_rate = 0.01 if vehicle.type == 'e_bike' else 0.02
    range_drain_rate = battery_drain_rate *0.1
    stop_thread = threading.Event()

    def update():
        while not stop_thread.is_set():
            current_time = timezone.now()
            elapsed_time = (current_time - rental.startTime).total_seconds()

            if rental.endTime or vehicle.batteryStatus <= 0:
                break

            vehicle.batteryStatus = max(0, vehicle.batteryStatus - battery_drain_rate)
            vehicle.range = max(0, vehicle.range - range_drain_rate)
            vehicle.save()

            time.sleep(1)

    thread = threading.Thread(target=update)
    thread.start()
    active_threads[rental.rentalID] = (thread, stop_thread)


@login_required
def start_rental(request, vehicle_id):
    if request.method == "POST":
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        vstartlocation = vehicle.location
        unpaid_rental = Rental.objects.filter(customer=request.user, endTime__isnull=False, payment__is_paid=False).first()
        ongoing_rental = Rental.objects.filter(customer=request.user, endTime__isnull=True).first()

        if unpaid_rental:
            return render(request, 'account.html', {
                'rentals': Rental.objects.filter(customer=request.user),
                'error': 'You have an unpaid rental. Please complete the payment before starting a new rental.'
            })
        if ongoing_rental:
            return render(request, 'account.html', {
                'rentals': Rental.objects.filter(customer=request.user),
                'error': 'You already have an ongoing rental. Please complete it before starting a new one.'
            })
        if vehicle.isDefective:
            return render(request, 'map.html', {'error': 'This vehicle is currently unavailable.'})

        rental = Rental.objects.create(
            vehicle=vehicle,
            customer=request.user,
            startTime=timezone.now(),
            startlocation=vstartlocation
        )
        vehicle.isDefective = True
        vehicle.save()
        Payment.objects.create(
            rental=rental,
            amount=0,
            is_paid=False
        )
        update_vehicle_status(rental)
        return redirect('moving', rental_id=rental.rentalID)
    return redirect('home')



def end_rental(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    vehicle = rental.vehicle
    all_locations = Location.objects.all()
    random_location = random.choice(all_locations)

    vehicle.location = random_location
    vehicle.position_x = random_location.position_x
    vehicle.position_y = random_location.position_y

    rental.endlocation = random_location

    rental.endTime = timezone.now()
    rental.save()

    if rental.rentalID in active_threads:
        thread, stop_thread = active_threads[rental.rentalID]
        stop_thread.set()
        thread.join()

    duration = rental.endTime - rental.startTime
    duration_in_minutes = duration.total_seconds() / 60
    rate = 1if rental.vehicle.type == 'e_bike' else 0.5
    cost = round(duration_in_minutes * rate, 2)

    payment = get_object_or_404(Payment, rental=rental)
    payment.amount = cost
    payment.save()

    rental.vehicle.isDefective = False
    rental.vehicle.save()

    return redirect('pay', rental_id=rental_id)

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

def pay(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    vehicle = rental.vehicle

    if request.method == 'GET':
        payment = get_object_or_404(Payment, rental=rental)
        return render(request, 'pay.html', {'payment': payment,'vehicle': vehicle})

    elif request.method == 'POST':
        rental = get_object_or_404(Rental, pk=rental_id)
        card_number = request.POST.get('card-number')
        expiry_date = request.POST.get('expiry-date')
        cvv = request.POST.get('cvv')

        payment = get_object_or_404(Payment, rental=rental)
        payment.cardNumber = card_number[-4:]
        payment.expiryDate = expiry_date
        payment.is_paid = True
        payment.save()

        rental.endTime = timezone.now()
        rental.save()

        vehicle.isDefective = False
        vehicle.save()
        return redirect('map')

    return render(request, 'pay.html', {'rental': rental, 'vehicle': vehicle})






def process_payment(request, payment_id):
    if request.method == "POST":

        card_number = request.POST.get('card-number')
        expiry_date = request.POST.get('expiry-date')
        cvv = request.POST.get('cvv')


        payment = get_object_or_404(Payment, pk=payment_id)


        payment.cardNumber = card_number[-4:]
        payment.expiryDate = expiry_date
        payment.is_paid = True
        payment.save()

        rental = payment.rental
        rental.endTime = timezone.now()
        rental.save()


        return redirect('map')

    return redirect('pay', rental_id=payment.rental.rentalID)


def account(request):
    rentals = Rental.objects.filter(customer=request.user)

    return render(request, 'account.html', {'rentals': rentals})

def rental_detail(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    try:
        payment = Payment.objects.get(rental=rental)
    except Payment.DoesNotExist:
        payment = None

    rental_data = {
        'rentalID': rental.rentalID,
        'vehicle_type': rental.vehicle.type,
        'start_time': rental.startTime,
        'end_time': rental.endTime,
        'payment_status': 'Paid' if payment and payment.is_paid else 'Not Paid',
        'amount': payment.amount if payment else 'N/A',
        'card_number': f"**** **** **** {payment.cardNumber[-4:]}" if payment else 'N/A',
        'expiry_date': payment.expiryDate if payment else 'N/A',
        'cvv': '***' if payment else 'N/A'
    }
    return JsonResponse(rental_data)


def complete_rental_view(request, rental_id):
    rental = get_object_or_404(Rental, rentalID=rental_id)

    if rental.customer == request.user:
        payment = rental.complete_rental()
        return redirect('payment_page', payment_id=payment.paymentID)

    return HttpResponse("You are not authorized to complete this rental.")


from .models import Payment

def payment_page(request, payment_id):
    payment = get_object_or_404(Payment, paymentID=payment_id)
    context = {
        'payment': payment,
    }
    return render(request, 'pay.html', context)



def complete_rental(self):
    try:
        payment = self.payment
        if payment.is_paid:
            return payment
    except Payment.DoesNotExist:
        pass

    self.endTime = timezone.now()
    self.save()

    amount = self.calculateCharges()

    payment, created = Payment.objects.get_or_create(
        rental=self,
        defaults={'amount': amount, 'is_paid': False}
    )

    if not created and not payment.is_paid:
        payment.amount = amount
        payment.save()

    return payment
def rental_detail_view(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    try:
        payment = Payment.objects.get(rental=rental)
    except Payment.DoesNotExist:
        payment = None

    context = {
        'rental': rental,
        'payment': payment,
    }
    return render(request, 'rental_detail.html', context)


def rental_detail_json(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    try:
        payment = Payment.objects.get(rental=rental)
    except Payment.DoesNotExist:
        payment = None

    rental_data = {
        'rentalID': rental.rentalID,
        'vehicle_type': rental.vehicle.type,
        'start_time': rental.startTime.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': rental.endTime.strftime('%Y-%m-%d %H:%M:%S') if rental.endTime else 'Ongoing',
        'payment_status': 'Paid' if payment and payment.is_paid else 'Not Paid',
        'amount': f"{payment.amount} USD" if payment else 'N/A',
        'card_number': f"**** **** **** {payment.cardNumber}" if payment else 'N/A',
        'expiry_date': payment.expiryDate if payment else 'N/A',
    }
    return JsonResponse(rental_data)

def rental_detail_page(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    try:
        payment = Payment.objects.get(rental=rental)
    except Payment.DoesNotExist:
        payment = None

    context = {
        'rental': rental,
        'payment': payment
    }
    return render(request, 'rental_detail.html', context)

class VehicleListView(APIView):
    def get(self, request):
        vehicles = Vehicle.objects.filter(position_x__isnull=False, position_y__isnull=False)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

from django.shortcuts import render, get_object_or_404

def moving_view(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    context = {
        'rental_id': rental_id,
    }
    return render(request, 'moving.html', context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Vehicle

@csrf_exempt
def charge_vehicle(request, vehicle_id):
    if request.method == 'POST':
        try:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
            vehicle.batteryStatus = 100
            vehicle.save()
            return JsonResponse({'success': True, 'message': f'Vehicle {vehicle_id} charged successfully.'})
        except Vehicle.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Vehicle not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


from django.shortcuts import render

def operator_dashboard(request):
    return render(request, 'operator.html')

def charge_vehicle_view(request):
    return render(request, 'charge_vehicle.html')



def repair_vehicle_view(request):

    defective_vehicles = Vehicle.objects.filter(isDefective=True)
    return render(request, 'repair_vehicle.html', {'defective_vehicles': defective_vehicles})

def repair_vehicle(request, vehicle_id):
    if request.method == 'POST':
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        vehicle.isDefective = False
        vehicle.batteryStatus = 100.0
        vehicle.save()

        return JsonResponse({'status': 'success', 'message': f'Vehicle {vehicle_id} repaired.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def get_vehicle_activities(request):
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')

    if not start_date or not end_date:
        return JsonResponse({"error": "Start and end dates are required."}, status=400)

    start_date = parse_date(start_date)
    end_date = parse_date(end_date)

    rentals = Rental.objects.filter(
        startTime__date__gte=start_date,
        endTime__date__lte=end_date
    ).select_related('vehicle', 'payment', 'customer')
    rental_data = []
    vehicle_data = []
    payment_data = []

    for rental in rentals:
        rental_data.append({
            'rentalID': rental.rentalID,
            'customer': rental.customer.username,
            'startTime': rental.startTime.strftime('%Y-%m-%d %H:%M:%S'),
            'endTime': rental.endTime.strftime('%Y-%m-%d %H:%M:%S') if rental.endTime else "Ongoing",
        })

        vehicle_data.append({
            'vehicleID': rental.vehicle.vehicleID,
            'type': rental.vehicle.type,
            'batteryStatus': rental.vehicle.batteryStatus,
            'location': rental.vehicle.location.address if rental.vehicle.location else "Unknown",
            'isDefective': rental.vehicle.isDefective,
            'position_x': rental.vehicle.position_x,
            'position_y': rental.vehicle.position_y,
        })
        if hasattr(rental, 'payment'):
            payment_data.append({
                'paymentID': rental.payment.paymentID,
                'amount': rental.payment.amount,
                'isPaid': rental.payment.is_paid,
                'cardNumber': rental.payment.cardNumber,
                'expiryDate': rental.payment.expiryDate,
            })

    operator_data = []
    manager_data = []
    customer_data = []

    operators = Operator.objects.all()
    for operator in operators:
        operator_data.append({
            'operatorID': operator.operatorID,
            'name': operator.name,
            'userType': operator.userType.name if operator.userType else "Unknown"
        })

    managers = Manager.objects.all()
    for manager in managers:
        manager_data.append({
            'managerID': manager.managerID,
            'name': manager.name,
            'userType': manager.userType.name if manager.userType else "Unknown"
        })



    return JsonResponse({
        'rentalData': rental_data,
        'vehicleData': vehicle_data,
        'paymentData': payment_data,
        'operatorData': operator_data,
        'managerData': manager_data,

    })


def track_vehicle(request):
    rentals = Rental.objects.select_related('vehicle', 'startlocation', 'endlocation')

    vehicles = Vehicle.objects.all()

    vehicle_data = []
    for rental in rentals:
        start_location = rental.startlocation
        end_location = rental.endlocation
        vehicle_data.append({
            'vehicleID': rental.vehicle.vehicleID,
            'rentalID': rental.rentalID,
            'type': rental.vehicle.type,
            'startTime': rental.startTime,
            'endTime': rental.endTime,
            'isDefective': rental.vehicle.isDefective,
            'start_longitude': start_location.position_x if start_location else None,
            'start_latitude': start_location.position_y if start_location else None,
            'end_longitude': end_location.position_x if end_location else None,
            'end_latitude': end_location.position_y if end_location else None,
        })

    return render(request, 'track_vehicle.html', {'vehicle_data': vehicle_data})

def move_vehicles(request):
    return render(request, 'move_vehicle.html')


@csrf_exempt
def move_vehicles(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vehicle_ids = data.get('vehicles')
        location_id = data.get('location_id')

        try:
            location = Location.objects.get(locationID=location_id)
        except Location.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Location not found'})

        vehicles = Vehicle.objects.filter(vehicleID__in=vehicle_ids)
        for vehicle in vehicles:
            vehicle.location = location
            vehicle.position_x = location.position_x
            vehicle.position_y = location.position_y
            vehicle.save()

        return JsonResponse({'success': True})

    elif request.method == 'GET':
        vehicles = Vehicle.objects.all()
        locations = Location.objects.all()
        return render(request, 'move_vehicle.html', {'vehicles': vehicles, 'locations': locations})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def visual_page(request):
    """
    Render the visual report page.
    """
    return render(request, 'visual.html')

def report_malfunction(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    vehicle.isDefective = True
    vehicle.save()

    payment = Payment.objects.filter(rental__vehicle=vehicle, is_paid=False).first()
    if payment:
        payment.is_paid = True
        payment.save()
    return JsonResponse({"status": "success", "message": "Vehicle reported as defective."})

def e_scooter_view(request):
    return render(request, 'E-Scooter.html')

def e_bike_view(request):
    return render(request, 'E-Bike.html')


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"From: {name} <{email}>\n\n{message}"

        # Send the email
        send_mail(
            subject,
            full_message,
            settings.EMAIL_HOST_USER,
            ['kkeeeekk8@gmail.com'],
            fail_silently=False,
        )

        # Return a JSON response to indicate success
        return JsonResponse({'success': True})

    return render(request, 'contact_us.html')


