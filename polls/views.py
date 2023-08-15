from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import View

from .forms import QuestionForm
from .models import Choice, Question


def index(request):
    # questions = Question.objects.order_by("-pub_date").all()

    # temp = loader.get_template("polls/index.html")
    # context = {"questions": questions}

    # return HttpResponse(temp.render(context, request))

    # questions = Question.objects.order_by("-pub_date").all()
    questions = (
        Question.objects.filter(pub_date__lte=timezone.now())
        .order_by("-pub_date")
        .all()
    )
    context = {"questions": questions}
    return render(request, "polls/index.html", context)


# Create your views here.
def detail(request, question_id):
    # ver. 1
    # return HttpResponse("You're looking at question %s." % question_id)
    # questions = Question.objects.filter(id=question_id)
    # if len(questions) == 0:
    #     return HttpResponse("Not Found")

    # question = questions[0]
    # context = {"question": question}
    # return render(request, "polls/detail.html", context)

    # ver. 2
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Ooops! Question not found")
    # context = {"question": question}
    # return render(request, "polls/detail.html", context)

    # ver. 3
    question = get_object_or_404(Question, pk=question_id, pub_date__lte=timezone.now())
    context = {"question": question}
    return render(request, "polls/detail.html", context)


def vote(request, question_id):
    choice_id = int(request.POST["choice"][0])

    choice = get_object_or_404(Choice, pk=choice_id)
    choice.votes += 1
    choice.save()

    # return HttpResponseRedirect("/polls/{{question_id}}")
    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(request, "polls/results.html", context)


class QuestionView(View):
    def get(self, request):
        form = QuestionForm()
        return render(request, "polls/question.html", {"form": form})

    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.pub_date = timezone.now() + timezone.timedelta(days=2)
            question.save()
            return HttpResponseRedirect(reverse("polls:index"))
        return render(request, "polls/question.html", {"form": form})


class QuestionEditView(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        form = QuestionForm(instance=question)
        return render(
            request,
            "polls/question_edit.html",
            {"form": form, "question_id": question_id},
        )

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)

        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("polls:detail", args=(question_id,)))
