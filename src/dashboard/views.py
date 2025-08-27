from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .utils import role_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Device
from .models import User
from rentals.models import *
from rentals.models import Rating, Device
from sentiment_analysis.sentiment_utils import analyze_sentiment
from django.http import JsonResponse
from collections import defaultdict

# Create your views here.

@role_required(allowed_roles=['seller'])
def seller_dashboard(request):
    return render(request, 'seller/Seller.html')


@login_required
def seller_products(request):
    devices = Device.objects.filter(owner=request.user)
    rentals = Rental.objects.filter(device__in=devices, buyer_returned=True, seller_confirmed__isnull=True)
    return render(request, 'seller/seller_products.html', {
        'devices': devices,
        'pending_confirmations': rentals
  })


@login_required
def add_device(request):
    if request.method == 'POST':
        name = request.POST.get('deviceName')
        specs = request.POST.get('deviceSpecs')
        price = request.POST.get('devicePrice')
        image = request.FILES.get('deviceImage')
        category = request.POST.get('deviceCategory')
        if name and specs and price and image and category:
            Device.objects.create(
                owner=request.user,
                name=name,
                specs=specs,
                price_per_day=price,
                image=image,
                category=category
            )
            return redirect('dashboard:seller_dashboard')  
        else:
            return render(request, 'seller/add_device.html', {
                'error': 'Please fill in all fields.'
            })

    return render(request, 'seller/add_device.html')


@login_required
def modify_device(request, device_id):
    device = get_object_or_404(Device, id=device_id, owner=request.user)

    if request.method == 'POST':
        name = request.POST.get('deviceName')
        specs = request.POST.get('deviceSpecs')
        price = request.POST.get('devicePrice')
        image = request.FILES.get('deviceImage')
        category = request.POST.get('deviceCategory')


        if name:
            device.name = name
        if specs:
            device.specs = specs
        if price:
            device.price_per_day = price
        if category:
            device.category = category
        if image:
            device.image = image

        device.save()
        return redirect('dashboard:seller_products')

    return render(request, 'seller/modify_device.html', {'device': device})



@login_required
def delete_device(request, device_id):
    device = get_object_or_404(Device, id=device_id, owner=request.user)
    
    if request.method == 'POST':
        device.delete()
        return redirect('dashboard:seller_products')  # بعد الحذف يرجع للقائمة

    # في حالة GET نعرض صفحة تأكيد الحذف
    return render(request, 'seller/con_delete_device.html', {'device': device})




@login_required
def delete_device_by_input(request):
    if request.method == 'POST':
        input_value = request.POST.get('device_input')

        # محاولة البحث بالـ ID أولًا، ثم بالاسم
        device = None
        if input_value.isdigit():
            device = Device.objects.filter(id=int(input_value), owner=request.user).first()
        else:
            device = Device.objects.filter(name__iexact=input_value.strip(), owner=request.user).first()

        if device:
            device.delete()
            messages.success(request, "Device deleted successfully.")
            return redirect('dashboard:seller_products')
        else:
            messages.error(request, "Device not found or you do not have permission to delete it.")

    return render(request, 'seller/delete_by_input.html')




@login_required
def modify_device_by_input(request):
    if request.method == 'POST':
        input_value = request.POST.get('deviceId')
        name = request.POST.get('deviceName')
        specs = request.POST.get('deviceSpecs')
        price = request.POST.get('devicePrice')
        image = request.FILES.get('deviceImage')

        # البحث عن الجهاز
        device = None
        if input_value.isdigit():
            device = Device.objects.filter(id=int(input_value), owner=request.user).first()
        else:
            device = Device.objects.filter(name__iexact=input_value.strip(), owner=request.user).first()

        if not device:
            messages.error(request, "Device not found or not owned by you.")
            return redirect('dashboard:modify_device_by_input')

        # تحديث فقط ما تم إدخاله
        if name:
            device.name = name
        if specs:
            device.specs = specs
        if price:
            device.price_per_day = price
        if image:
            device.image = image

        device.save()
        messages.success(request, "Device updated successfully.")
        return redirect('dashboard:seller_products')

    return render(request, 'seller/modify_device_by_input.html')








@role_required(allowed_roles=['manager'])
def manager_dashboard(request):
    ratings = Rating.objects.all()
    sentiments = {"positive": 0, "negative": 0, "neutral": 0}
    for rating in ratings:
        sentiment = analyze_sentiment(rating.comment)
        sentiments[sentiment] += 1
    return render(request, 'management/Manager.html', {"sentiments": sentiments})


CATEGORY_CHOICES = {
    'computers': 'Computers',
    'televisions': 'Televisions',
    'projectors': 'Projectors',
    'printers': 'Printers',
    'cameras': 'Cameras',
    'speakers': 'Speakers',
}
def manager_sentiment_dashboard(request):
    categorized_devices = defaultdict(list)
    devices = Device.objects.all()

    for device in devices:
        ratings = Rating.objects.filter(device=device)
        sentiments = {"positive": 0, "negative": 0, "neutral": 0}
        comments_data = []

        for rating in ratings:
            sentiment = analyze_sentiment(rating.comment)
            sentiments[sentiment] += 1
            comments_data.append({
                "comment": rating.comment,
                "sentiment": sentiment.capitalize()
            })

        categorized_devices[device.get_category_display()].append({
            "name": device.name,
            "sentiments": sentiments,
            "comments": comments_data
        })

    return render(request, "management/Manager.html", {"categorized_devices": dict(categorized_devices)})

@role_required(['manager'])
@login_required
def manage_users(request):
    users = User.objects.exclude(role='manager')  # لا تعرض المديرين
    return render(request, 'management/UsersManagement.html', {'users': users})

@role_required(['manager'])
@login_required
def manage_devices(request):
    devices = Device.objects.all()
    return render(request, 'management/DevicesManagement.html', {'devices': devices})

@role_required(['manager'])
@login_required
def delete_user(request, user_id):
    user = User.objects.filter(id=user_id).exclude(role='manager').first()
    if user:
        user.delete()
    return redirect('dashboard:manage_users')

@role_required(['manager'])
@login_required
def delete_device_admin(request, device_id):
    device = Device.objects.filter(id=device_id).first()
    if device:
        device.delete()
    return redirect('dashboard:manage_devices')






@role_required(allowed_roles=['buyer'])
def buyer_dashboard(request):
    return render(request, 'buyer/buyer.html')





@role_required(allowed_roles=['buyer'])
@login_required
def my_rentals(request):
    rentals = Rental.objects.filter(user=request.user).select_related('device')
    return render(request, 'buyer/devices_buyer.html', {'rentals': rentals})

@role_required(allowed_roles=['buyer'])
@login_required
def rate_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    return render(request, 'buyer/rating.html', {'device': device})
 
from django.http import JsonResponse
import json




@require_POST
@login_required
def submit_review(request):
    try:
        data = json.loads(request.body)
        comment = data.get('comment')
        stars = int(data.get('stars'))
        device_id = data.get('device_id')

        device = Device.objects.get(id=device_id)

        Rating.objects.create(
            device=device,
            user=request.user,
            comment=comment,
            stars=stars
        )

        return JsonResponse({'message': 'Review submitted successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@login_required
@role_required(['buyer'])
def mark_as_returned(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    rental.buyer_returned = True
    rental.save()
    return redirect('dashboard:my_rentals')

@login_required
@role_required(['seller'])
def confirm_return(request, rental_id, decision):
    rental = get_object_or_404(Rental, id=rental_id, device__owner=request.user)
    if decision == 'yes':
        rental.seller_confirmed = True
        rental.status = 'returned'  # ✅ تحديث حالة الإيجار
        rental.device.is_available = True  # ✅ جعل الجهاز متاح مرة ثانية
        rental.device.save()
    else:
        rental.seller_confirmed = False  # ✅ في حالة الرفض فقط
    rental.save()

    return redirect('dashboard:seller_products')
