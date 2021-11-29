from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from license import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('addcustomer/', views.addcustomer, name='addcustomer'),
    path('addlic/', views.addlic, name='addlic'),
    path('list/<str:company>/', views.infocomp, name='infocomp'),
    path('sendmail/<str:company>/', views.sendmail, name='sendmail'),
    path('delete/', views.delete, name='delete'),
    path('create/', views.create, name='create'),
    path('logout/', views.logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
