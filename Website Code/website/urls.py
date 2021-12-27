from django.urls import path,include
from . import views

extra_patterns=[
    path('summary/',views.summary,name="summary"),

]
urlpatterns = [
    path('', views.Home.as_view(),name=''),
    #path('', views.index, name='index'),
    path('TextUpload/',views.upload,name="TextUpload"),
    path('TextUpload/',include(extra_patterns)),
    path('MediaUpload/',views.mediaUpload,name="MediaUpload"),
    path('MediaUpload/',include(extra_patterns)),

    
]


