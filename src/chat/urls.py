from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signin/', views.SigninView.as_view(), name="signin"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('signup/', views.signup, name="signup"),
]