from django.shortcuts import render, redirect
from .models import ContactMessage
from django.contrib import messages

# Create your views here.


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        project = request.POST.get('project')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                project=project,
                subject=subject,
                message=message
            )
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact:contact_us') 
        else:
            messages.error(request, 'Please fill out the required fields.')

    return render(request, 'contact_us.html')

def terms_of_use(request):
    return render(request, 'terms_of_use.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')