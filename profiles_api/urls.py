from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profiles_api import views


# Specifically for ViewSet example
router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset') # base_name is for internal purposes
router.register('profile', views.UserProfileViewSet) # don't need base name because we specified the queryset in the viewset. This defaults to the model name in question.

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),  # as_view() allows APIView class to be rendered by our URLs
    path('', include(router.urls)), # include is imported from django.urls. Blank string because we don't want to include a prefix.
]