from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import User
from .forms import RegistrationForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages


# Create your views here.


def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        # البحث في البريد أو الاسم أو رقم الهوية
        user_obj = (
            User.objects.filter(email=identifier).first()
            or User.objects.filter(username=identifier).first()
            or User.objects.filter(id_number=identifier).first()
        )

        if user_obj:
            user = authenticate(request, email=user_obj.email, password=password)
            if user:
                login(request, user)
                messages.success(request, "Logged in successfully!")

                # توجيه حسب نوع المستخدم
                if user.role == 'seller':
                    return redirect('dashboard:seller_dashboard')
                elif user.role == 'manager':
                    return redirect('dashboard:manager_dashboard')
                return redirect('dashboard:buyer_dashboard')

        messages.error(request, "Invalid login credentials. Please try again.")
        return render(request, 'regester/login.html')

    return render(request, 'regester/login.html')



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        else:
            print(" Form is NOT valid")
            print(form.errors)  # هذا هو المفتاح
    else:
        form = RegistrationForm()
    return render(request, 'regester/register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile/profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
        else:
            print(form.errors)
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'profile/edit_profile.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('rentals:home')
