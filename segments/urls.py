from rest_framework.routers import DefaultRouter
from segments.views import SegmentViewSet, UserViewSet

router = DefaultRouter()
router.register(r'segments', SegmentViewSet, basename='segment')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls
