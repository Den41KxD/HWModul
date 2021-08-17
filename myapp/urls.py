from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [

    path('accounts/profile/', NoteListViewForLogin.as_view(), name='index'),
    path('',NoteListViewNotLogin.as_view(),name='NotLog'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('buyTovar/<int:pk>',TovarBuy.as_view(),name='TovarBuy'),
    path('note/create/', NoteCreateView.as_view(), name='note-create'),
    path('note/update/<int:pk>/', UpdateNote.as_view(), name='note-updade'),
    path('adminindex/',NoteListViewForLogin.as_view(),name='AdminIndex'),
    path('mybuy/',MyBuyView.as_view(),name='mybuy'),
    path('mybuy/<int:pk>',ReturnOneBuy.as_view(),name='mybuy'),
    path('returncheck/',ReturnCheck.as_view(),name='returncheck'),
    path('returncheck/<int:pk>',NotReturn.as_view(),name='notreturncheck'),
    path('acceptreturncheck/<int:pk>',AcceptReturn.as_view(),name='acceptreturncheck'),
    path('admin/', admin.site.urls),
]
