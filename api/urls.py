from django.urls import path
from api.views import (
    RegisterView,
    LoginView,
    ProfileView,
    MessageListCreateView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('messages/', MessageListCreateView.as_view(), name='messages'),
]
