from django.urls import path,include
from . import views

extra_patterns=[
    path('summary',views.summary,name="summary"),
    path('transcriptsPreview',views.transcriptsPreview,name="transcriptsPreview"),
    path('notes/',views.notes,name="notes"),
    path('notes/gen_notes',views.gen_notes,name="gen_notes"),


]
urlpatterns = [
    path('', views.home,name=''),
    #path('', views.index, name='index'),
    path('TextUpload/',views.upload,name="TextUpload"),
    path('TextUpload/',include(extra_patterns)),
    path('MediaUpload/',views.mediaUpload,name="MediaUpload"),
    path('MediaUpload/',include(extra_patterns)),
    # path('transcripts/',include(extra_patterns)),

    path('accounts/login',views.login,name='login'),
    
    path('accounts/login/verification/',views.phone_verification, name='phone_verification'),
    path('verification/token/',views.token_validation, name='token_validation'),
    path('verified/',views.verified, name='verified'),  

    path('textUpload/',views.textUpload,name="textUpload"),
    path('textUpload/',include(extra_patterns)),
    path('mediaUpload/',views.mediaUpload,name="mediaUpload"),
    path('mediaUpload/',include(extra_patterns))



    
]


