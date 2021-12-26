from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(),name=''),
    #path('', views.index, name='index'),
    path('upload/',views.upload,name="upload"),
    path('upload/summary',views.summary,name="summary"),
    # path('summary/', views.summary,name='summary')
]
