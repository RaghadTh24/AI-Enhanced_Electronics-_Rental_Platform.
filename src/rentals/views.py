from django.contrib import messages

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.utils import role_required
from dashboard.models import Device
from .models import *
from datetime import datetime,timedelta
from .models import DeviceNotification  
from datetime import date
from rest_framework import viewsets
from .models import Device
from .serializers import DeviceSerializer

# Create your views here.
def home(request):
    latest_devices = Device.objects.filter(is_available=True).order_by('-created_at')[:3]  # أحدث 6 أجهزة
    return render(request, 'home.html', {
        'latest_devices': latest_devices
    })



class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


def products(request):
    return render(request,'products.html')


def category_devices(request, category_slug):
    devices = Device.objects.filter(category=category_slug)  # لا نقيّد بالتوفر
    category_name = category_slug.capitalize()
    
    return render(request, 'category_devices.html', {
        'devices': devices,
        'category': category_name,
    })







@role_required(allowed_roles=['buyer'])
@login_required

def device_detail(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    ratings = Rating.objects.filter(device=device).select_related('user')
    similar_devices = Device.objects.filter(
        category=device.category,
        is_available=True
    ).exclude(id=device.id)[:3]

    # تحقق مما إذا كان الجهاز عليه حجز جاري الآن (بناء على التاريخ)
    is_currently_rented = Rental.objects.filter(
        device=device,
        start_date__lte=date.today(),
        end_date__gte=date.today(),
        status='confirmed'
    ).exists()

    # استقبال البريد للإشعار إذا كان مستأجرًا حاليًا
    if request.method == 'POST' and is_currently_rented:
        email = request.POST.get('notify_email')
        if email:
            DeviceNotification.objects.get_or_create(device=device, email=email)
            messages.success(request, "You will be notified when this device becomes available.")
            return redirect('rentals:device_detail', device_id=device.id)

    return render(request, 'device_detail.html', {
        'device': device,
        'ratings': ratings,
        'similar_devices': similar_devices,
        'is_currently_rented': is_currently_rented,
    })
@role_required(allowed_roles=['buyer'])
@login_required
def payment_page(request, device_id):
    device = get_object_or_404(Device, id=device_id)

    # قراءة عدد الأيام من LocalStorage (إن وجد) أو تعيين افتراضي
    rental_days = int(request.GET.get('rental_days', 1))
    start_date = datetime.today().date()
    end_date = start_date + timedelta(days=rental_days)
    

    # تحقق من وجود حجوزات متداخلة
    overlapping_rentals = Rental.objects.filter(
        device=device,
        end_date__gte=start_date,
        start_date__lte=end_date,
    ).exclude(status='returned')

    if overlapping_rentals.exists():
        return render(request, 'device_detail.html', {
            'device': device,
            'error_message': "Sorry, this device is already rented during the selected period."
        })
    total_price = device.price_per_day * rental_days
    return render(request, 'payment.html', {
        'device': device,
        'rental_days': rental_days,
        'total_price':total_price
    })




@role_required(allowed_roles=['buyer'])
@login_required
def confirm_rental(request, device_id):
    device = get_object_or_404(Device, id=device_id)

    if request.method == 'POST':
        rental_days = int(request.POST.get('rental_days', 1))
        payment_method = request.POST.get('payment_method')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')

        # تحقق من الحجوزات المتداخلة
        start_date = datetime.today().date()
        end_date = start_date + timedelta(days=rental_days)

        overlapping_rentals = Rental.objects.filter(
            device=device,
            end_date__gte=start_date,
            start_date__lte=end_date,
        ).exclude(status='returned')

        if overlapping_rentals.exists():
            error_message = "Sorry, this device is already rented during the selected period."
            return render(request, 'device_detail.html', {
                'device': device,
                'error_message': error_message
            })

        # احسب السعر الكلي
        total_price = device.price_per_day * rental_days

        # إنشاء الحجز
        Rental.objects.create(
            user=request.user,
            device=device,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            payment_method=payment_method,
            location_lat=lat,
            location_lng=lng,
            status='confirmed'
        )

        return redirect('rentals:order_summary')

    return redirect('rentals:payment', device_id=device.id)



@role_required(allowed_roles=['buyer'])
@login_required
def order_summary(request):
    last_rental = Rental.objects.filter(user=request.user).order_by('-id').first()

    if not last_rental:
        return redirect('rentals:products')

    return render(request, 'order_summary.html', {'rental': last_rental})



# views.py
from django.db.models import Q

def search_devices(request):
    keyword = request.GET.get('keyword', '')
    category = request.GET.get('category', '')

    results = Device.objects.filter(is_available=True)

    if keyword:
        results = results.filter(Q(name__icontains=keyword) | Q(specs__icontains=keyword))
    if category:
        results = results.filter(category__iexact=category)

    return render(request, 'search_results.html', {
        'devices': results,
        'keyword': keyword,
        'category': category,
    })








from django.core.mail import send_mail
from .models import DeviceNotification

def notify_users_if_available(device):
    if device.is_available:
        notifications = DeviceNotification.objects.filter(device=device, notified=False)
        for n in notifications:
            send_mail(
                subject="Device Available for Rent",
                message=f"The device '{device.name}' is now available at RentTech. Visit the site to rent it!",
                from_email="noreply@renttech.com",
                recipient_list=[n.email],
                fail_silently=True,
            )
            n.notified = True
            n.save()

@role_required(['buyer'])
@login_required
def return_device(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)

    rental.buyer_returned = True
    rental.save()

    # 💥 إرسال إشعارات لمن طلب إشعار عند توفر الجهاز
    notify_users_if_available(rental.device)

    messages.success(request, 'Device marked as returned.')

    return redirect('dashboard:my_rentals')



def similar_available_devices(request, category_slug):
    exclude_id = request.GET.get('exclude')  # معرف الجهاز الذي نريد استبعاده
    devices = Device.objects.filter(
        category=category_slug,
        is_available=True
    )
    if exclude_id:
        devices = devices.exclude(id=exclude_id)

    return render(request, 'similar_devices.html', {
        'devices': devices,
        'category': category_slug.capitalize()
    })
