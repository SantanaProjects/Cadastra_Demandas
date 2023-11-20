
from django.urls import path,include
from .views import user_login, criar_demanda,cadastro,custom_logout


urlpatterns = [
  
    path('', user_login, name='user_login'),
    path('criar_demanda/', criar_demanda, name='criar_demanda'),
    path('cadastro', cadastro, name='cadastro'),
    path('logout/', custom_logout, name='logout'),
]


