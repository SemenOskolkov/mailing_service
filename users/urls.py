from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserLoginView, UserRegisterView, RegisterSuccessView, UserProfileView, UserPasswordChangeView, \
    user_activation, simple_reset_password, UsersListView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('register/success/', RegisterSuccessView.as_view(), name='register_success'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    # path('password/', UserPasswordChangeView.as_view(), name='change_password'),
    path('activate/<str:token>/', user_activation, name='activate'),
    path('simple/reset/', simple_reset_password, name='simple_reset'),
    path('users_list/', UsersListView.as_view(), name='users_list')
]