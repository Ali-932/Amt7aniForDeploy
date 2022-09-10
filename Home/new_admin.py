from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline, AdminSite

import Home
from .models import Profile, Stage, Question, Chapters, Subjects, Quiz, UserQuizzes
from django import forms
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

ADMIN_ORDERING = {
    "Home": [
        "Profile",
        "Stage",
        "Subjects",
        "Quiz",
        "Question",
        "UserQuizzes"
    ],
}


def get_app_list(self, request):
    app_dict = self._build_app_dict(request)
    for app_name, object_list in app_dict.items():
        if app_name in ADMIN_ORDERING:
            app = app_dict[app_name]
            app["models"].sort(
                key=lambda x: ADMIN_ORDERING[app_name].index(x["object_name"])
            )
            app_dict[app_name]
            yield app
        else:
            yield app_dict[app_name]


admin.AdminSite.get_app_list = get_app_list


# Register your models here.
class StageinLine(admin.TabularInline):
    model = Stage


@admin.register(Profile)
class ClothesAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'gender',
        'created',
        'modified',
        'id',
        'show_average')

    def show_average(self, obj):

        return Profile.get_avg_score(obj)

    list_filter = ('user', 'created', 'modified')
    search_fields = ('name',)
    inlines = [
        StageinLine,
    ]


class Stageform(forms.ModelForm):
    class Meta:
        model = Stage
        exclude = ('profile',)


@admin.register(Stage)
class StageAdmin(SuperModelAdmin):
    form = Stageform
    list_display = ('id', 'stages', 'profile', 'type')
    list_filter = ('stages',)


class ChapterInLine(admin.TabularInline):
    model = Chapters


@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stage')
    list_filter = ('stage',)
    search_fields = ('name',)
    inlines = [
        ChapterInLine,
    ]


class quizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = "__all__"


class QuestionInlineAdmin(SuperInlineModelAdmin, StackedInline):
    model = Question
    extra = 0


@admin.register(Quiz)
class QuizAdmin(SuperModelAdmin):
    list_display = ('id', 'name', 'stage', 'subject', 'chapter', 'timer')
    list_filter = ('stage', 'subject', 'chapter')
    search_fields = ('name', 'chapter', 'stage')

    inlines = (QuestionInlineAdmin,)
    form = quizForm


@admin.register(Question)
class QuestionAdmin(SuperModelAdmin):
    list_display = (
        'id',
        'questionBody',
        'quiz',
        'isProblem',
        'choiceA',
        'choiceB',
        'choiceC',
        'image',
    )
    list_filter = ('quiz', 'isProblem')

@admin.register(UserQuizzes)
class ua(admin.ModelAdmin):
    pass