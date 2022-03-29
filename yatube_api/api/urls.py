from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token
)


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

# router.register(
#     r'posts/(?P<post_id>\d+)/comments/(?P<comment_id>\d+)',
#     CommentViewSet, basename='single_comment'
# )

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/jwt/create/', obtain_jwt_token),
    path('v1/jwt/refresh/', refresh_jwt_token),
    path('v1/jwt/verify/', verify_jwt_token),
]
