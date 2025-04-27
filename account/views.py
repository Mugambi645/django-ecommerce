from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from orders.views import user_orders

from .forms import RegistrationForm, UserEditForm
from .models import UserBase
from .tokens import account_activation_token


@login_required
def dashboard(request):
    """
    Display the user dashboard with their profile information and order history.
    """
    orders = user_orders(request)
    return render(request,
                  'account/user/dashboard.html',
                  {'section': 'profile', 'orders': orders})

from django.contrib import messages

@login_required
def edit_details(request):
    """
    Allow users to edit their profile details (except email and username).
    """
    form_submitted = False  # NEW LINE

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
            form_submitted = True  # NEW LINE
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/user/edit_details.html',
                  {'user_form': user_form, 'form_submitted': form_submitted})  # NEW LINE

@login_required
def delete_user(request):
    """
    Deactivate the current user's account and log them out.
    """
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_register(request):
    """
    Handle user registration process:
    - Create an inactive user.
    - Send an email with an activation link.
    """
    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered successfully and activation sent')
    else:
        registerForm = RegistrationForm()
        
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    """
    Activate the user's account after verifying the activation link.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserBase.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')
