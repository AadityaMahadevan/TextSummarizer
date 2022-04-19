from django.urls import path,include
from . import views

extra_patterns=[
    path('summary/',views.summary,name="summary"),

]
urlpatterns = [
    path('', views.home,name=''),

    #path('', views.index, name='index'),
    path('TextUpload/',views.upload,name="TextUpload"),
    path('TextUpload/',include(extra_patterns)),
    path('MediaUpload/',views.mediaUpload,name="MediaUpload"),
    path('MediaUpload/',include(extra_patterns)),
    path('MediaUpload1/',views.mediaUpload,name="MediaUpload1"),
    path('MediaUpload1/',include(extra_patterns)),
    path('accounts/login',views.login,name='login'),


    path('textUpload/',views.textUpload,name="textUpload"),
    path('mediaUpload/',views.mediaUpload,name="mediaUpload")



    
]


