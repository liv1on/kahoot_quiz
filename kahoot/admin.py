from django.contrib import admin
from . import models


@admin.register(models.User)
class UsersDisplay(admin.ModelAdmin):
    list_display = [
        'name',
        'second_name',
        'email',
        'list_of_groups',
        'phone_number',
        'overall_score',
    ]
    list_display_links = ['email']
    list_filter = ['groups']
    search_fields = ['name', 'second_name', 'phone_number']
    ordering = ['raiting']
    readonly_fields = ['passed_quiz', 'raiting', 'raiting_group']





@admin.register(models.Leader)
class LeaderDisplay(admin.ModelAdmin):
    list_display = [
        'name',
        'second_name',
        'email',
        'list_of_groups',
        'phone_number',
        'raiting',
        'overall_score',
        'passed_quiz',
    ]
    list_filter = ['groups']
    search_fields = ['name', 'second_name', 'phone_number']
    ordering = ['raiting']
    readonly_fields = ['passed_quiz', 'raiting', 'raiting_group']
    list_display_links = ['email']





class UserInline(admin.TabularInline):
    model = models.User
    fields = [
        'email',
        'id'
    ]




class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]
    inlines = [
        UserInline
    ]




@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'list_of_groups_quizzes'
    ]




class AnswerInlineModels(admin.TabularInline):
    model = models.Answer
    max_num = 4
    min_num = 4
    fields = [
        'answer_title',
        'is_corect'
    ]




@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    extra = 4
    fields = [
        'title',
        'quiz',
        'image',
        'timer',
        'score',
        'answer_score',
    ]
    list_display = [
        'title',
        'get_quizzes',
        'date_updated',
    ]

    inlines = [
        AnswerInlineModels
    ]


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):

    list_display = [
        'answer_title',
        'is_corect',
        'question'
    ]
