from django.urls import path, include
from . import views

urlpatterns = [
    path('spit/', views.SpitView.as_view()),
    path('spit/<int:pk>/', views.SpitDetailView.as_view()),
    path('spit/<int:pk>/children/', views.SpitListView.as_view()),
    path('spit/<int:pk>/collect/', views.SpitCollectView.as_view()),
    path('spit/<int:pk>/updatethumbup/', views.SpitUpdatethumbupView.as_view()),
]
