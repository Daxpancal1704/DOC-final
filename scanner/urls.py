from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.home, name='home'),

    path('document/', views.document_scanner, name='document'),

    path('image/', views.image_scanner, name='image_scanner'),
    # path('text/', views.text_analyzer, name='text'),

    path('register/', views.register_view, name='register'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('text/', views.text_analyzer, name='text_analyzer'),

    path('history/', views.scan_history, name='scan_history'),

    path('report/<int:id>/', views.scan_report, name='scan_report'),

    path('download/<int:id>/', views.download_report, name='download_report'),

    path('delete/<int:id>/', views.delete_scan, name='delete_scan'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)