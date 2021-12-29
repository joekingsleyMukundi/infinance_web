from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='userLogin'),
    path('', views.dashboardUser, name='userDashboard'),
    path('logout/', views.logoutUser, name='userlogout'),
    path('register/', views.registerUser, name='registerUser'),
    path('email_verification/', views.emailVerification, name='emailVrification'),
    path('reminders/', views.remindersUser, name='reminders'),
    path('transactions/', views.transactionsUser, name='transaction'),
    path('deletetransaction/<str:pk>',
         views.deletetransaction, name='deletetransaction'),
    path('mycards/', views.usercards, name='usercards'),
    path('loadwallet/', views.depositeUser, name='deposite'),
    path('sendmoney/', views.sendMoneyUser, name='sendmoney'),
    path('withdraw/', views.withdrawUser, name='withdraw'),
    path('deletereminder/<str:pk>/', views.deleteReminder, name='deleteReminder')
]
