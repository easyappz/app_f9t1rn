from django.urls import path
from api.views import (
    HelloView,
    RegisterView,
    LoginView,
    ProfileView,
    MessagesListView,
    MessageCreateView
)

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("messages/", MessagesListView.as_view(), name="messages-list"),
    path("messages/", MessageCreateView.as_view(), name="message-create"),
]
