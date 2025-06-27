from django.urls import path
from . import views

urlpatterns = [
    path('authorize', views.auth),
    path('logout-user', views.logout_user),
    path('get-user-data', views.get_user_data),
    path('user-verify', views.user_verify),

    path('get-cartridges-data', views.get_cartridges_data),
]