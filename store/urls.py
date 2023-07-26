from django.urls import path
from .views import *


urlpatterns = [
    path('category/', CategoryView.as_view()),
    path('category/<int:id>/', CategoryView.as_view()),
]