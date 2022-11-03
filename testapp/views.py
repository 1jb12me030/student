from django.shortcuts import render

# Create your views here.


from django.shortcuts import render


from django.shortcuts import render
from .serializers import ChatSerializer
from .models import Chat
from rest_framework import viewsets
from rest_framework.views import APIView
from django.db import transaction
from chatbot.models import Questionaire,Questions,Responses
from rest_framework import status
from rest_framework.response import Response
from django.db.models.functions import Concat
from django.db.models import Value

from django.contrib.auth.models import Permission
from rest_framework.authtoken.models import Token
from django.http.response import JsonResponse
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAdminUser
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import random
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.cache import cache


# Registration Api:
class RegistrationView(APIView):       
    def get(self, request):
        try:
            username = request.GET.get('username')
            # print("username:",username)
            if cache.get(username):
                print('data from cache')
                register = cache.get(username)
                return JsonResponse(register, safe=False)
            else:
                if username:
                    obj = Registration.objects.filter(username=username).first()
                    if obj:
                        serializer = RegistrationSerializer(obj)
                        cache.set(serializer.data['username'], serializer.data)
                        return Response(data=serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'Username not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)





# Post data:
    def post(self, request):
        try:
            data = request.data
            serializer = RegistrationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
                
                # user=Registration.objects.get(username=serializer.data['username'])
                # refresh = RefreshToken.for_user(user)
                # return Response({'status':200,'payload':serializer.data,'refresh':str(refresh)

                                #  'access': str(refresh.access_token),'message':'your data is saved'})
            else:
                return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            print(e)
            return Response({'message': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)








# Update all things:
    def patch(self, request):
        try:
            username = request.GET.get('username')
            print("username:",username)
            data = request.data
            print("data:",data)
            if username:
                obj = Registration.objects.filter(username=username).first()
                if obj:
                    serializer = RegistrationSerializer1(obj, data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(data=serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    return Response({'message': 'Username not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'Username is empty please provide username'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'message': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)








# Login Api:
class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                username = serializer.data['username']
                password = serializer.data['password']
                register = Registration.objects.filter(
                    username=username).first()
                if register:
                    if username and password:
                        user = authenticate(
                            username=username, password=password)
                        if user:
                            # return JsonResponse(register,safe=False)
                            s = RegistrationSerializer(register)
                            refresh = RefreshToken.for_user(user)
                            return Response({'status':200,"data":serializer.data,'refresh':str(refresh),

                                 'access': str(refresh.access_token),'message':'Login Sucessfully'})
                            
                        else:                        
                            return Response({'message': 'Invalid username and password'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    else:
                        return Response({
                            'message': 'username and password required'
                        }, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            print(e)
            return Response({
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)







# Logout Api:
class LogOutView(APIView):
    def post(self, request):
        try:
            logout(request)
            return Response({'message': 'logout'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'something went to wrong'}, status=status.HTTP_400_BAD_REQUEST)







class ChatView(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer



class ChatTreeView(APIView):

    @transaction.atomic
    def insertions(self, chat_nodes, questionaire_name):
        try:

            with transaction.atomic():
                # Create Questionaire
                questionaire = Questionaire(name=questionaire_name)
                questionaire.save()

                options = []
                for node in chat_nodes:

                    # Create Questions
                    question = Questions(question_text=node["question"], reference_id=node["id"], questionaire=questionaire)
                    question.save()                 #question id required

                    for response, next in node["response"].items():
                        options.append(
                            Responses(options=response, next=next, question=question, questionaire=questionaire))

                # Create Responses
                Responses.objects.bulk_create(options)          #bulk insert all response options


        except:
            return False

        return True


    def post(self,request):

        #data validation
        if 'file' not in request.FILES or 'name' not in request.data:
            return Response("Insufficient Parameters",status=status.HTTP_400_BAD_REQUEST)

        if not request.FILES['file'].name.lower().endswith('.json'):
            return Response("Invalid File",status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


        import json

        file_obj = request.FILES['file']
        file_obj.seek(0)
        data = file_obj.read()

        try:
            data = json.loads(data)
        except:
            return Response("Invalid Json",status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        #inserting decoded json
        if self.insertions(data,request.data["name"]):
            return Response("File inserted",status=status.HTTP_201_CREATED)

        return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ChatbotView(APIView):
    def post(self,request):

        if 'questionaire' not in request.data:
            return Response("Insufficient Parameters",status=status.HTTP_400_BAD_REQUEST)

        try:
            questionaire = Questionaire.objects.get(id=request.data["questionaire"])
        except Questionaire.DoesNotExist:
            return Response("Invalid Questionaire", status=status.HTTP_400_BAD_REQUEST)


        #If the status for last conversation is Null indicate the conversation was conpleted, else active conversation for questionaire

        try:
            chat = Chat.objects.get(questionaire=questionaire,status__isnull= False)
        except Chat.DoesNotExist:
            chat = None


        #A new chat
        if not chat:
            question = Questions.objects.get(reference_id=1,questionaire=questionaire)

            try:
                Chat.objects.create(questionaire=questionaire,log=question.question_text)
            except:
                return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        else:
            question = Questions.objects.get(reference_id=chat.status,questionaire=questionaire)

            count = Responses.objects.filter(question=question.id, questionaire=questionaire)[:1] #check if there more stages in Conversation

            if not count:
                Chat.objects.filter(id=chat.id).update(status=None)     #ending conversation by setting status to null
                return Response("Restarting Conversation: "+chat.log, status=status.HTTP_200_OK)

            if "message" not in request.data:
                return Response("Invalid input", status=status.HTTP_400_BAD_REQUEST)

            valid_response = Responses.objects.filter(question=question.id,questionaire=questionaire,options__iexact=request.data["message"])[:1] #check if the user chose a valid option
            if not valid_response:
                return Response("Invalid Option", status=status.HTTP_400_BAD_REQUEST)

            try:
                question = Questions.objects.get(reference_id=valid_response[0].next,questionaire=questionaire) #fetch next question for user
            except Questions.DoesNotExist:
                return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            Chat.objects.filter(id=chat.id).update(status=question.reference_id,log=Concat('log', Value("->"+request.data["message"]))) #update chat state

        options = Responses.objects.values_list('options',flat=True).filter(question=question.id) #fetch option for current question

        result = {
            "question" : question.question_text,
            "response" : options
        }


        return Response(result,status=status.HTTP_200_OK)