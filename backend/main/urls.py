from django.urls import path
from . import views

urlpatterns = [
    path('authorize', views.auth),
    path('logout-user', views.logout_user),
    path('get-user-data', views.get_user_data),
    path('user-verify', views.user_verify),

    path('get-cartridges-data', views.get_cartridges_data),
    path('get-cartridge-data-to-edit', views.get_cartridge_data_to_edit),
    path('get-cartridge-models', views.get_cartridge_models),
    path('get-departments', views.get_departments),
    path('get-the-found-cartridges', views.get_the_found_cartridges),

    path('add-new-cartridge', views.add_new_cartridge),

    path('update-cartridge-data', views.update_cartridge_data),

    path('generate-barcode-pdf', views.generate_barcode_pdf),
]