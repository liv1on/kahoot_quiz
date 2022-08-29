from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.decorators import  APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import generics

from .models import *
from .serializers import *
from .service import create_raiting, create_raiting_group, calculate_point


class UserLISTView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_details = User.objects.all()
        serializer = UserSerializer(user_details, many=True)
        return Response(serializer.data)


class SearchByParams(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'second_name', 'phone_number']



class UserLISTViewTop(APIView):
    def get(self, request):
        user_details = User.objects.alias(score=Count('overall_score')).order_by('-overall_score')
        serializer = UserSerializer(user_details, many=True)
        create_raiting(user_details)
        return Response(serializer.data)


class UserLISTViewTopByGroup(APIView):
    def get(self, request, **kwargs):
        user_details = User.objects.filter(groups__name=kwargs['group_name']).order_by('-overall_score')[:3]
        serializer = UserSerializer(user_details, many=True)
        create_raiting_group(request, **kwargs)
        return Response(serializer.data)


class UserSearchNameView(APIView):
    def get(self, request, **kwargs):
        user_details = User.objects.filter(name=kwargs['user_name'])
        serializer = UserSerializer(user_details, many=True)
        return Response(serializer.data)


class UserSearchLastNameView(APIView):
    def get(self, request, **kwargs):
        user_details = User.objects.filter(last_name=kwargs['user_last_name'])
        serializer = UserSerializer(user_details, many=True)
        return Response(serializer.data)


class UserSearchPhoneView(APIView):
    def get(self, request, **kwargs):
        user_details = User.objects.filter(telephone_number=kwargs['phone'])
        serializer = UserSerializer(user_details, many=True)
        return Response(serializer.data)




class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer)
    def post(self, request):
        data = request.data
        serializer = RegisterUserSerializer(data=data)
        print(request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully signed up', status=status.HTTP_201_CREATED)


class ActivateView(APIView):
    def get(self, request, activation_code):
        User = get_user_model()
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response("Your account was successfully activated", status=status.HTTP_200_OK)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logged out', status=status.HTTP_200_OK)

class ActivateView(APIView):
    def get(self, request, activation_code):
        User = get_user_model()
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response("Your account was successfully activated", status=status.HTTP_200_OK)



class GroupByUserAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = GroupSerializer

    def get(self, request):
        results = Group.objects.filter(user=request.user)
        serializer = GroupSerializer(results, many=True)
        print(request.user.replied_questions_and_scores)
        return Response(serializer.data)


class QuizByUserAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        queryset = Quiz.objects.filter(group__in=request.user.groups.all())
        serializer = QuizSerializer(queryset, many=True)
        print(request.user.name)
        return Response(serializer.data)


class GetValidQuestionsAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = AnswersSerializer

    def get_queryset(self):
        answer_id = self.request.data.get("answer_id")
        answer = Answer.objects.get(id=answer_id)
        print(answer_id, answer)
        return answer

    def post(self, request, quiz_id, question_id, **kwargs):
        answer = self.get_queryset()
        time_answer = request.data.get('answer_time')
        calculate_point(request, answer, time_answer, question_id)
        return Response('Your answer has been submitted')





