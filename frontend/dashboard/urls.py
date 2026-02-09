from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    path('nueva-medicion/', views.NuevaMedicionView.as_view(), name='nueva_medicion'),
    path('mediciones-auto/', views.MedicionesAutoView.as_view(), name='mediciones_auto'),
    path('api/mediciones-auto/', views.MedicionesAutoAPIView.as_view(), name='mediciones_auto_api'),
    path('auto/', views.AutoView.as_view(), name='auto'),
    path('mediciones/', views.MedicionesListView.as_view(), name='mediciones'),
    path('mediciones/<int:pk>/', views.MedicionDetailView.as_view(), name='medicion_detalle'),
    path('reportes/', views.ReportesView.as_view(), name='reportes'),
    path('configuracion/', views.ConfiguracionView.as_view(), name='configuracion'),
]
