from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from issueTracker.views import SignupUserView, ProjectListView

router = routers.SimpleRouter()
router.register(r'projects', ProjectListView, basename="projects")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/signup/', SignupUserView.as_view({'post': 'create'}), name='signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/projects/', ProjectListView.as_view({'get': 'list', 'post': 'create'}), name='projects'),
    # path('api/projects/<int:pk>/', ProjectDetailView.as_view({'get': 'retrieve'})),
]