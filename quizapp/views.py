from django.shortcuts import render, redirect
from .models import Quiz , Choice
from .forms import QuizForm

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizapp/quizlist.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    total_questions = quiz.question_set.count()  # Calculate the total number of questions

    if request.method == 'POST':
        form = QuizForm(quiz, request.POST)
        if form.is_valid():
            user_responses = {}
            score = 0

            for question in quiz.question_set.all():  # Use quiz.question_set
                question_id = f"question_{question.id}"
                user_response_id = form.cleaned_data.get(question_id)

                # Get the corresponding Choice object for the user's response
                user_response = Choice.objects.get(pk=user_response_id)

                # Check if the user's response is correct
                if user_response.is_correct:
                    score += 1

                # Store the user's response in the dictionary
                user_responses[question.text] = user_response.text

            # Provide feedback to the user
            return render(request, 'quizapp/quiz_result.html', {'score': score, 'user_responses': user_responses, 'total_questions': total_questions})

    else:
        form = QuizForm(quiz)

    return render(request, 'quizapp/quizdetail.html', {'quiz': quiz, 'form': form})



def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')
    else:
        form = QuizForm()
        
    return render(request,'quizapp/create_quiz.html',{'form':form})    