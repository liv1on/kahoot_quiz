from .models import Question, Quiz, User

def calculate_point(request, answer, answer_time, question_id):

    question_in_subject = Question.objects.get(id=question_id)
    timer_m = question_in_subject.timer
    score_m = question_in_subject.score

    if answer.is_corect:
        if timer_m > answer_time:
            request.user.question_score = round(score_m * (1 - answer_time / timer_m), 1)
            request.user.save()
        else:
            request.user.question_score = 0
            request.user.save()
    else:
        request.user.question_score = 0
        request.user.save()


    record_of_scores = request.user.answer_table
    record_of_scores[str(question_id)] = request.user.question_score  #record of responses
    request.user.total_score = sum(record_of_scores.values())
    print(record_of_scores)

    all_quizzes = request.user.quizzes_and_answers # all tests


    number_quizzes = Quiz.objects.filter(group__in=request.user.groups.all())  # all tests user


    for item in number_quizzes:
        number_questions = []
        for element in Question.objects.filter(quiz__id=item.id):
            number_questions.append(str(element.id))
        all_quizzes[str(item.id)] = number_questions
    request.user.save()
    print(all_quizzes)                     #comparison of the test and with the answer

    submitted_answers_string = []
    for item in record_of_scores.keys():
        submitted_answers_string.append(item)
    print(submitted_answers_string)
    print("All quizzes are ", all_quizzes)

                                                  #  Count passed tests
    count_passed_tests = 0
    for item in all_quizzes:
        if set(all_quizzes[item]).issubset(submitted_answers_string):
            print(all_quizzes[item])
            passed_quiz = passed_quiz + 1

    print(count_passed_tests)
    request.user.passed_quiz = passed_quiz
    request.user.answer_table = record_of_scores

    request.user.save()
    return request.user.question_score


def create_raiting(user_details):  # raiting

    raiting = 1
    for item in user_details:
        item.ranking = raiting
        item.save()
        print(item, raiting)
        raiting = raiting + 1


def create_raiting_group(request, **kwargs): #raiting group

    user_details = User.objects.filter(groups__name=kwargs['group_name']).order_by('-overall_score')
    raiting = 1
    for item in user_details:
        item.raiting_group = raiting
        item.save()
        print(item, raiting)
        raiting = raiting + 1

from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    activation_url = f'http://localhost:8000/registration/activate/{activation_code}'
    message = f'Thank you for signing up. Please activate your account.' \
              f'Pleas follow the link below: {activation_url}'
    send_mail('Activate your account',
              message,
              'registration@admin.com',
              [email, ],
              fail_silently=False
              )
