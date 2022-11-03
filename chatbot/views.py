from django.shortcuts import render

# Create your views here.
from .serializers import QuestionaireSerializer,QuestionsSerializer,ResponsesSerializer
from .models import Questionaire,Questions,Responses
from rest_framework import viewsets

class QuestionaireView(viewsets.ModelViewSet):
    queryset = Questionaire.objects.all()
    serializer_class = QuestionaireSerializer


class QuestionsView(viewsets.ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer


class ResponsesView(viewsets.ModelViewSet):
    queryset = Responses.objects.all()
    serializer_class = ResponsesSerializer


