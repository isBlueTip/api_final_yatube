from rest_framework_jwt.views import obtain_jwt_token


from django.urls import include, path

from rest_framework.routers import SimpleRouter
# from rest_framework.authtoken import views

from .views import PostViewSet#, GroupViewSet, CommentViewSet

router = SimpleRouter()

router.register('posts', PostViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/api-token-auth/', obtain_jwt_token),
    path('v1/jwt/create/', obtain_jwt_token),
]
