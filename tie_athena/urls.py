from django.contrib import admin
from django.urls import include, path

from learn_aim_check.views import LearnCheckChart, LearnCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('drf_auth.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/learn-check', LearnCheckView.as_view(), name='learn-check'),
    path('api/v1/learn-check/<int:pk>/', LearnCheckView.as_view(), name='learn_check_patch'),
    path('api/v1/learn-check/chart/<int:pk>/', LearnCheckChart.as_view(), name='learn_check_chart'),
]
