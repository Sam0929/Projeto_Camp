from django.urls import path
from .views import HomeView, profile, RegisterView, CustomLoginView

urlpatterns = [
    path('', HomeView.as_view(), name='login'),  # Página de login   
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
]
