from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from . import views


app_name = 'users'

router = DefaultRouter()
router.register(r'', views.UserViewSet, basename='users')

urlpatterns = [
    path(r'api/v1/password-reset/', include('django_rest_resetpassword.urls', namespace='password_reset')),
    path('api/v1/', include(router.urls)),
    path('api/v1/token/', views.CustomObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('hello/', views.HelloView.as_view(), name='hello'),
]
