from rest_framework_jwt.views import obtain_jwt_token


from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import PostViewSet, GroupViewSet, CommentViewSet

router = SimpleRouter()

router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet, basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/jwt/create/', obtain_jwt_token),
]
