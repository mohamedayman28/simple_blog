from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm

from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='posts:home_page'), name='logout'),
    path('signup/', views.user_form, name='signup'),
    path('user-update/<id>/', views.user_form, name='user_update'),
]
