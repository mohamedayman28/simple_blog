from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.contrib.auth import views as auth_views, login

from accounts.forms import CreateUserForm


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = 'accounts/login.html'
    # Redirect to home page if try to access URL(accounts:login).
    redirect_authenticated_user = True
    success_message = 'You have loggedin successfully!'

    extra_context = {'title': 'Login'}

    def get_success_url(self):
        return reverse('posts:home_page')


def user_form(request, id=None):
    # Make user that id held integer.
    try:
        id = int(id)
    except Exception:
        id = None

    # At the top for multiple usage.
    context = {}

    # If update account request.
    if id and request.resolver_match.url_name == 'update':
        user = get_object_or_404(User, id=id)
        # Add values to dictionary(context)
        context['title'] = 'Update informations'
        context['form'] = CreateUserForm(request.POST or None, instance=user)
        # Assign user, to login after validate the form.
        context['user'] = user
        context['msg'] = 'Account has been updated.'
    # If signup request.
    else:
        context['title'] = 'Signup'
        context['form'] = CreateUserForm(request.POST or None)
        context['msg'] = 'Account created successfully.'

    if request.method == 'POST':
        form = context.get('form')
        msg = context.get('msg')
        user = context.get('user')

        if form.is_valid():
            form.save()
            messages.success(request, msg)
            # Login user
            #   Redirect to home page by default after login, using the
            # declared CBV LoginView.method(redirect_authenticated_user).
            if bool(user):
                login(request, user)
            return redirect('accounts:login')

    return render(request, 'accounts/login.html', context)
