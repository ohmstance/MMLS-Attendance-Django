from django.urls import path, include

from . import views

app_name = 'acc'
urlpatterns = [
    path('', views.AccountView.as_view(), name='account'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('user_delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('config/', views.ConfigView.as_view(), name='config'),
]

# urlpatterns = [
#     path('', views.AccountView.as_view(), name='account'),
#     path('login/', views.LoginView.as_view(), name='login'),
#     path('register/', views.RegisterView.as_view(), name='register'),
#     path('logout/', LogoutView.as_view(), name='logout')
# ]

# urlpatterns = [
#     # ex: /polls/
#     path('', views.index, name='index'),
#     # ex: /polls/5/
#     path('<int:question_id>/', views.detail, name='detail'),
#     # ex: /polls/5/results/
#     path('<int:question_id>/results', views.results, name='results'),
#     # ex: /polls/5/vote/
#     path('<int:question_id>/vote', views.vote, name='vote'),
# ]