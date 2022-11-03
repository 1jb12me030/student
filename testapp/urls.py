from django.urls import path
from .views import *




urlpatterns = [
    path('register/',RegistrationView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogOutView.as_view()),
    
    path('chattree/',ChatTreeView.as_view(),name="chattree"),
    path('chatbot/',ChatbotView.as_view(),name="chatbot")
    
    
]