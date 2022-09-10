import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import CheckConstraint, Q, F, Avg, Count

User = get_user_model()


class Gender():
    male = 'Male'
    famale = 'Female'
    gender = (
        (male, 'Male'),
        (famale, 'Female')
    )


class TimeChoices():
    min_5 = '5'
    min_10 = '10'
    min_15 = '15'
    min_20 = '20'
    min_25 = '25'
    min_30 = '30'
    min_35 = '35'
    min_40 = '40'
    min_45 = '45'
    min_50 = '50'
    min_55 = '55'
    min_60 = '60'
    timeChoices = ((min_5, '5:00'),
                   (min_10, '10:00'),
                   (min_15, '15:00'),
                   (min_20, '20:00'),
                   (min_25, '25:00'),
                   (min_30, '30:00'),
                   (min_35, '35:00'),
                   (min_40, '40:00'),
                   (min_45, '45:00'),
                   (min_50, '50:00'),
                   (min_55, '55:00'),
                   (min_60, '60:00'))


class StageChoices():
    stage1 = 'اول ابتدائي'
    stage2 = 'ثاني ابتدائي'
    stage3 = 'ثالث ابتدائي'
    stage4 = 'رابع ابتدائي'
    stage5 = 'خامس ابتدائي'
    stage6 = 'سادس ابتدائي'
    stage7 = 'اول متوسط'
    stage8 = 'ثاني متوسط'
    stage9 = 'ثالث متوسط'
    stage10 = 'رابع اعدادي'
    stage11 = 'خامس اعدادي'
    stage12 = 'سادس اعدادي'

    stages = (
        (stage1, 'اول ابتدائي'),
        (stage2, 'ثاني ابتدائي'),
        (stage3, 'ثالث ابتدائي'),
        (stage4, 'رابع ابتدئي'),
        (stage5, 'خامس ابتدائي'),
        (stage6, 'سادس ابتدائي'),
        (stage7, 'اول متوسط'),
        (stage8, 'ثاني متوسط'),
        (stage9, 'ثالث متوسط'),
        (stage10, 'رابع اعدادي'),
        (stage11, 'خامس اعدادي'),
        (stage12, 'سادس اعدادي'),

    )


class StageType():
    schientific = "علمي"
    literary = "ادبي"
    biologiocal = "احيائي"
    engineerical = "تطبيقي"
    none = 'لا يوجد'
    types = (
        (schientific, 'علمي'),
        (literary, 'ادبي'),
        (biologiocal, 'احيائي'),
        (engineerical, 'تطبيقي'),
        (none, "لا يوجد"),

    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=35)
    gender = models.CharField(max_length=255, choices=Gender.gender)
    created = models.DateTimeField(auto_now_add=True, )
    modified = models.DateTimeField(auto_now=True, )
    id = models.AutoField(primary_key=True, )
    stage = models.ForeignKey("Stage", on_delete=models.SET_NULL, null=True, blank=True, related_name="profile_stage")

    def Update_profile(self, name, gender, stage, ):
        self.name = name
        self.gender = gender
        new_stage = Stage.objects.get(stages=stage)
        self.stage = new_stage
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = "Profile"
        verbose_name_plural = 'Profiles'
        # constraints = [
        #     CheckConstraint(
        #         check = Q(end_date__gt=F('start_date')),
        #         name = 'check_start_date',
        #     ),
        # ]


class Stage(models.Model):
    stages = models.CharField(max_length=255, choices=StageChoices.stages, null=False, blank=False)
    type = models.CharField(max_length=255, choices=StageType.types, default=StageType.none)

    def __str__(self):
        if self.type != StageType.none:
            return str(self.stages + " " + self.type)
        else:
            return self.stages

    class Meta:
        verbose_name = 'Stage'
        verbose_name_plural = 'Stages'
        unique_together = ("stages", "type",)

    def get_subjects(self):  # new
        return Subjects.objects.filter(stage=self)


class Subjects(models.Model):
    name = models.CharField(max_length=25)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, related_name='subject_stage')

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.name

    def get_chapters(self):  # new
        return Chapters.objects.filter(subject=self)
        # <QuerySet [<Chapters: فصل اول>, <Chapters: فصل ثاني>]>


class Chapters(models.Model):
    name = models.CharField(max_length=255, blank=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='chapter_subject', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'


class Quiz(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, related_name='quiz_stage')
    subject = models.ForeignKey(Subjects, on_delete=models.SET_NULL, null=True, related_name='quiz_subject')
    chapter = models.ForeignKey(Chapters, on_delete=models.SET_NULL, related_name='quiz_chapter',
                                null=True)  # manyTomany
    timer = models.CharField(choices=TimeChoices.timeChoices, max_length=255)
    created = models.DateTimeField(auto_now_add=True, )
    q_num = models.IntegerField(default=0)  # change to 10 after questions are set

    def __str__(self):
        return self.name

    def get_questions(self):
        questions = Question.objects.filter(quiz_id=self.id).order_by('?')[:self.q_num]

        return questions

    def get_All_questions(self, subject, stage):
        questions = Question.objects.filter(quiz__subject=subject, quiz__stage=stage).order_by('?')
        # <QuerySet [<Question: ماهي علاقه المقاومه بلكهرباء>, <Question: ماهي علاقه عناصر الماء>, <Question: ماهي علاقه الهواء بلماء>, <Question: عرف الماء>]>
        return questions


class Question(models.Model):
    questionBody = models.CharField(max_length=255, blank=True, null=True)
    # ChoiceA = models.CharField(max_length=255, blank=True, null=True)
    # a_isTure = models.BooleanField(default=False)
    # ChoiceB = models.CharField(max_length=255, blank=True, null=True)
    # b_isTure = models.BooleanField(default=False)
    # ChoiceC = models.CharField(max_length=255, blank=True, null=True)
    # c_isTure = models.BooleanField(default=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, related_name='question_quiz', null=True, blank=True)
    isProblem = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True, )
    # extra = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return "%s" % self.questionBody


class choices(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, related_name='choices_question', null=True,
                                 blank=True)
    choiceBody = models.CharField(max_length=70, blank=True, null=True)
    isCorrect = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)



class UserQuizzes(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='profile_userquizzes')
    created = models.DateTimeField(auto_now_add=True, )  # created from front
    subject = models.ForeignKey(Subjects, on_delete=models.SET_NULL, related_name="subject_userquizzes", null=True)
    chapter = models.ForeignKey(Chapters, on_delete=models.SET_NULL, related_name="chapter_userquizzes", null=True)
    score = models.IntegerField(default=0, editable=False)

    def get(self):
        get_created = self.created
        get_subject = self.subject
        get_chapter = self.chapter
        get_score = self.score
        return {
            'created': get_created,
            'subject': get_subject,
            'chapter': get_chapter,
            'score': get_score,
        }


class UserScoring(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='profile_scoring')
    total_score_points = models.IntegerField(default=0, editable=False)
    total_right_choices = models.IntegerField(default=0, editable=False)

    def get_avg_score(self):
        avg_score = self.total_right_choices / self.total_score_points
        return str(avg_score * 100) + '%'

# django_loger
