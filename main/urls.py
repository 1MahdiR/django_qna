from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:q_id>/', views.question, name="question"),
    path('submit/', views.question_submit, name="submit"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
]

