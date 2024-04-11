from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F

from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"questions": latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': f"선택이 없습니다. id={request.POST['choice']}"})
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args={question_id,}))

def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})

class SingupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('user-list') ## user를 만든 뒤 특정 url로 보내줌
    template_name = 'registration/signup.html'

