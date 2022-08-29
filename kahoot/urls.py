from django.urls import path
from . import views

app_name = 'kahoot'


urlpatterns = [
    path('users/', views.UserLISTView.as_view(), name="list-of-users"),
    path('users/search', views.SearchByParams.as_view()),
    path('registration/', views.RegisterUserView.as_view()),
    path('registration/activate/<str:activation_code>/', views.ActivateView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('users/leaders_global', views.UserLISTViewTop.as_view()),
    path('users/leaders_group/<str:group_name>/', views.UserLISTViewTopByGroup.as_view()),
    path('users/search/name/<str:user_name>/', views.UserSearchNameView.as_view()),
    path('users/search/last_name/<str:user_last_name>/', views.UserSearchLastNameView.as_view()),
    path('users/search/phone/<str:phone>/', views.UserSearchPhoneView.as_view()),
    path('quiz/groups', views.GroupByUserAPIView.as_view()),
    path('quiz/list', views.QuizByUserAPIView.as_view()),
    path('quiz/<int:quiz_id>/<int:question_id>/', views.GetValidQuestionsAPIView.as_view())
]