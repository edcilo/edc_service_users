from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('api/v1/token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('hello', views.HelloView.as_view(), name='hello'),
]
