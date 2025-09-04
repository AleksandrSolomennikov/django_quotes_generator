from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_quote, name='add_quote'),
    path('vote/<int:pk>/', views.vote_quote, name='vote_quote'),
    path('top10/', views.top10, name='top10'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sources/add/', views.add_source, name='add_source'),
    path("signup/", views.signup, name="signup"),
    path('dashboard/filter/', views.dashboard_filter, name='dashboard_filter'),
]