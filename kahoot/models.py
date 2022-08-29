from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin, Group
import hashlib
from kahoot.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):


    name = models.CharField(max_length=100, blank=True)
    second_name = models.CharField(max_length=100, default="", blank=True)
    email = models.EmailField(unique=True, primary_key=True)
    phone_number = models.IntegerField(null=True, blank=True)
    question_score = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    answer_table = models.JSONField(default=dict, null=True, blank=True)
    overall_score = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    raiting = models.PositiveSmallIntegerField(editable=False, null=True, blank=True)
    raiting_group = models.PositiveSmallIntegerField(editable=False, null=True, blank=True)
    passed_quiz = models.PositiveSmallIntegerField(default=0, blank=True)
    is_staff = models.BooleanField(default=False)
    quizzes_and_answers = models.JSONField(default=dict, null=True, blank=True)


    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["email"]



    USERNAME_FIELD = 'email'
    objects = UserManager()



    def __str__(self):
        return self.email

    def list_of_groups(self):
        print(self.groups.all(), type(self.groups.all()))
        return ', '.join(map(str, self.groups.all()))





class Quiz(models.Model):

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    title = models.CharField(max_length=255, verbose_name="Quiz Title")
    group = models.ManyToManyField(Group, related_name="group_quizzes")

    def list_of_groups_quizzes(self):
        return ', '.join(map(str, self.group.all()))

    def __str__(self):
        return self.title


class Updated(models.Model):
    date_updated = models.DateTimeField(
        verbose_name="Last updated", auto_now=True)
    class Meta:
        abstract = True


class Question(Updated):
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    quiz = models.ManyToManyField(Quiz, related_name='question')
    title = models.CharField(max_length=255, verbose_name="Title")
    image = models.ImageField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    timer = models.FloatField(default=20.0, help_text="Maximum allowed time for question")
    answer_score = models.FloatField(default=0, help_text="Score for the answer")
    score = models.FloatField(default=100.0, help_text="Maximum score", blank=True)
    is_active = models.BooleanField(default=False, verbose_name="Active Status")

    def get_quizzes(self):
        return "\n".join([q.title for q in self.quiz.all()])

    def __str__(self):
        return self.title


class Answer(Updated):
    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ["id"]

    question = models.ForeignKey(Question, related_name="answer", on_delete=models.DO_NOTHING)
    answer_title = models.CharField(max_length=255, verbose_name="Answer Text")
    response_timer = models.FloatField(default=20.0, help_text="Time take to answer")
    answer_score = models.PositiveSmallIntegerField(default=100, help_text="Score for the answer")
    is_corect = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


class Leader(User):
    class Meta:
        verbose_name = "Leader"
        verbose_name_plural = "Leaders"
        proxy = True



    def create_activation_code(self):

        string = str(self.email) + str(self.groups)
        encode_string = string.encode()
        md5_object = hashlib.md5(encode_string)
        activation_code = md5_object.hexdigest()
        self.activation_code = activation_code