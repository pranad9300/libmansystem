from django.urls import path,include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
urlpatterns = [
    # path('', TemplateView.as_view(template_name='social_app/login.html')),
    path('sign_up', views.sign_up, name="sign_up"),
    path('login/',views.login,name="login"),
    path('createuser',views.createuser,name="createuser"),
    path('handle_login',views.handle_login,name="handle_login"),
    path('index',views.index,name="index"),
    path('logout',views.logout,name="logout"),
    path('profile_filup',views.profile,name="profile_fillup"),
    path('createprofile',views.createprofile,name="createprofile"),
    path('activate/<uidb64>/<token>',views.Verification_view.as_view(),name='activate'),
    path('forgot_password',views.forgotPassword,name="forgot_password"),
    path('send_otp',views.send_otp,name="send_otp"),
    path('check_otp',views.check_otp,name="check_otp"),
    path('changepassword',views.change_password,name="changepassword")
]