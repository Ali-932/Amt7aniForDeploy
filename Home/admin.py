from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline, AdminSite
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from nested_admin.nested import NestedModelAdmin, NestedTabularInline, NestedStackedInline

from .models import Profile, Stage, Question, Chapters, Subjects, Quiz, UserQuizzes, choices
from django import forms
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin
User = get_user_model()


#

ADMIN_ORDERING = {
    "Home": [
        "Profile",
        "Stage",
        "Subjects",
        "Quiz",
        "Question",
        "UserQuizzes",
        "Chapters"
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

#
admin.AdminSite.get_app_list = get_app_list


@admin.register(Chapters)
class Chapteradmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ClothesAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'gender',
        'stage',
        'created',
        'modified',
        'id',
        # 'show_average'
    )

    def show_average(self, obj):

        return obj.profile_scoring.get_avg_score()
    list_filter = ('user', 'created', 'modified','stage')
    search_fields = ('name',)



@admin.register(Stage)
class StageAdmin(SuperModelAdmin):
    list_display = ('id', 'stages', 'type','view_students_link')
    list_filter = ('stages',)


    def view_students_link(self, obj):
        count = obj.profile_stage.count()
        url = (
                reverse("admin:Home_profile_changelist")
                + "?"
                + urlencode({"stage__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Students</a>', url, count)

    view_students_link.short_description = "Students"


class ChapterInLine(admin.TabularInline):
    model = Chapters
    extra = 0

#event_listener
# @admin.register(Chapters)
# class ch(admin.ModelAdmin):
#     list_display = ('id', 'name', 'subject')
#     list_filter = ('subject','stage')
#     search_fields = ('name',)

@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stage','view_chapter_count')
    list_filter = ('stage',)
    search_fields = ('name',)
    inlines = [
        ChapterInLine,
    ]


    #class Media:


    def view_chapter_count(self, obj):
        count = obj.chapter_subject.count()
        return (str(count) +' Chapters')

    view_chapter_count.short_description = "Chapters"


class ChoiceInlineAdmin(NestedStackedInline):
    model = choices
    extra = 1

class QuestionInlineAdmin(NestedStackedInline):
    model = Question
    extra = 0
    inlines = [ChoiceInlineAdmin]

@admin.register(Quiz)
class QuizAdmin(NestedModelAdmin):
    list_display = ('id', 'name', 'stage', 'subject'
                    # ,'chapter'
                    , 'timer','view_questions_link')
    list_filter = ('stage', 'subject', 'chapter')
    search_fields = ('name', 'chapter', 'stage')
    inlines = [QuestionInlineAdmin,]
    # def get_queryset(self, request):
    #     qs = super(QuizAdmin, self).get_queryset(request)
    #     return qs.exclude(name="ALLQ932")


    def view_questions_link(self, obj):
        count = obj.question_quiz.count()
        url = (
                reverse("admin:Home_question_changelist")
                + "?"
                + urlencode({"quiz__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{}</a>', url, count)

    view_questions_link.short_description = "questions"

@admin.register(Question)
class QuestionAdmin(NestedModelAdmin):
    inlines = [ChoiceInlineAdmin]
    list_display = (
        'id',
        'questionBody',
        'quiz',
        'isProblem',
        'stage_name',
        'subject_name',
        'chapter_name'
    )
    list_filter = ('quiz', 'isProblem',)

    # def add_to_quiz_action(modeladmin,request, queryset):
    #     quiz=Quiz.objects.get(question_quiz__in=queryset)
    #     queryset.update(quiz=quiz)
    def subject_name(self,obj):
        if obj.quiz:
            return obj.quiz.subject.name
        else: return None
    subject_name.short_description = 'Subject name'
    def chapter_name(self,obj):
        if obj.quiz:
            return obj.quiz.chapter.name
        else: return None

    subject_name.short_description = 'Subject name'
    def stage_name(self,obj):
        if obj.quiz:
            return obj.quiz.subject.stage.stages
        else: return None

    subject_name.short_description = 'stage name'

