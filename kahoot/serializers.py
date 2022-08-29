import django.contrib.auth.models
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, Quiz, Question, Answer
from .service import send_activation_code


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = django.contrib.auth.models.Group
        fields = ('name','id')


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['name', 'second_name', 'email', 'phone_number',
                  'overall_score', 'raiting', 'raiting_group', 'passed_quiz', 'groups']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['answer_title', 'is_corect', 'id']


class QuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'answer']
        depth = 1


class QuizSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'group', 'title', 'question']


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=1, write_only=True, help_text="Minimum length of a password is 1")
    password_confirmation = serializers.CharField(min_length=1, write_only=True)

    def validate_email(self, login):
        if User.objects.filter(email=login).exists():
            raise serializers.ValidationError("This email is busy")
        return login

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirmation']

    def validate(self, validated_data):
        print(validated_data)
        password = validated_data.get('password')
        password_confirmation = validated_data.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Passwords don t match')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = User.objects.create_user(email=email, password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code)

        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={"input_type": "password"},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), login=email, password=password)

            if not user:
                message = 'Incorrect login or password'
                raise serializers.ValidationError(message, code="authorization")

        else:
            message = 'Must include "email" and "password".'
            raise serializers.ValidationError(message, code="authorization")
        attrs['user'] = user
        return attrs


class AnswersSerializer(serializers.Serializer):
    answer_id = serializers.IntegerField(required=True)
    answer_time = serializers.IntegerField(required=True)





