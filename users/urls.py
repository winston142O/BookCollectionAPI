from django.urls import path
from .views import signup, login_view, get_user_details

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('me/', get_user_details, name='get_user_details'),
]
