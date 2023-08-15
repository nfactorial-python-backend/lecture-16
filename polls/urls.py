from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    #
    path("", views.index, name="index"),
    path("<int:question_id>/details", views.detail, name="detail"),
    path("<int:question_id>/vote", views.vote, name="vote"),
    path("<int:question_id>/results", views.results, name="results"),
    path("questions/", views.QuestionView.as_view(), name="question"),
    path(
        "questions/<int:question_id>",
        views.QuestionEditView.as_view(),
        name="question_edit",
    ),
    #
]
