from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'tracks', views.TrackViewSet)
router.register(r'trackpoints', views.TrackPointViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^upload/', views.FileUploadView.as_view(), name ='upload'),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework'))
]
