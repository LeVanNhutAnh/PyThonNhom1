from django.urls import path
from . import views

app_name = 'App'

urlpatterns = [
    path('', views.home, name='home'),
    path('chat-demo/', views.chat_demo, name='chat_demo'),
    path('ai-chat/', views.ai_chat, name='ai_chat'),
    path('analyze-document/', views.analyze_document, name='analyze_document'),
    path('whisper-transcribe/', views.whisper_transcribe, name='whisper_transcribe'),
]