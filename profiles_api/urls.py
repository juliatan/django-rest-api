from django.urls import path

from profiles_api import views


urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),  # as_view() allows APIView class to be rendered by our URLs
]