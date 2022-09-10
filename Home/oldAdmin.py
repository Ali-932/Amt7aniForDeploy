# from django.contrib import admin
# from django.contrib.admin import TabularInline, StackedInline
#
# from .models import Profile, Stage, Question, Chapters, Subjects, Quiz, choices
# from django import forms
# from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin
#
#
# # Register your models here.
# class StageinLine(admin.TabularInline):
#     model = Stage
#
#
# @admin.register(Profile)
# class ClothesAdmin(admin.ModelAdmin):
#     inlines = [
#         StageinLine,
#     ]
#
# class ChapterInLine(admin.TabularInline):
#     model = Chapters
#
#
# @admin.register(Subjects)
# class SubjectsAdmin(admin.ModelAdmin):
#     inlines = [
#         ChapterInLine,
#     ]
#
#
# # class Questioninline(admin.TabularInline):
# #     model = choices
# #
# #
# #
# #
# # class Quizinline(admin.TabularInline):
# #     model = Question
#
#
# class quizForm(forms.ModelForm):
#     class Meta:
#         model = Quiz
#         fields="__all__"
#     # def __init__(self, *args, **kwargs):
#     #     super(quizForm, self).__init__(*args, **kwargs)
#     #     self.fields['subject'].queryset = Subjects.objects.filter(stage_id=self.instance.stage_id)
# class ChoiceInlineAdmin(SuperInlineModelAdmin, TabularInline):
#     model = choices
#
# class QuestionInlineAdmin(SuperInlineModelAdmin, StackedInline):
#     model = Question
#     inlines = (ChoiceInlineAdmin,)
#
#
#
# @admin.register(Quiz)
# class QuizAdmin(SuperModelAdmin):
#     inlines = (QuestionInlineAdmin,)
#
#     form = quizForm
#
# @admin.register(Question)
# class QuestionAdmin(SuperModelAdmin):
#     inlines = [ChoiceInlineAdmin]
