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
    none='لا يوجد'
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
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier', )
    def get_avg_score(self):
        avg_score=UserQuizzes.objects.filter(user=self).aggregate(Avg('score'))
        return avg_score['score__avg']
    def total_quizzes(self):
        total_quiz=UserQuizzes.objects.filter(user=self).aggregate(Count("id"))
        return total_quiz['id__count']
    def Update_profile(self, name,gender,):
        profile=Profile.objects.get(id=self.id)
        profile.name=name
        profile.save(['name'])
        profile.gender=gender
        profile.save(['gender'])

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['id']
        verbose_name = "Profile"
        verbose_name_plural='Profiles'
        # constraints = [
        #     CheckConstraint(
        #         check = Q(end_date__gt=F('start_date')),
        #         name = 'check_start_date',
        #     ),
        # ]


class Stage(models.Model):
    stages = models.CharField(max_length=255, choices=StageChoices.stages,null=False,blank=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=255, choices=StageType.types, null=True, blank=True,default=StageType.none)
    def Update_stage(self, new_stage,):
        stage=Stage.objects.get(id=self.id)
        stage.name=new_stage

    def __str__(self):
        if self.type != StageType.none:
            return str(self.stages + " " + self.type)
        else:
            return self.stages

    class Meta:
        verbose_name = 'Stage'
        verbose_name_plural = 'Stages'


class Subjects(models.Model):
    name = models.CharField(max_length=25)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, related_name='subject_stage')

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.name


class Chapters(models.Model):
    name = models.CharField(max_length=255, blank=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='chapter_subject',null=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, related_name='quiz_stage')
    subject = models.ForeignKey(Subjects, on_delete=models.SET_NULL, null=True, related_name='quiz_subject')
    chapter = models.ForeignKey(Chapters, on_delete=models.SET_NULL, related_name='quiz_chapter', null=True)
    timer = models.CharField(choices=TimeChoices.timeChoices, max_length=255)

    def __str__(self):
        return self.name


class Question(models.Model):
    questionBody = models.CharField(max_length=255, blank=True, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, related_name='question_quiz', null=True, blank=True)
    choiceA = models.CharField(max_length=255, blank=True, null=True)
    choiceA_isCorrect=models.BooleanField(default=False)
    choiceB = models.CharField(max_length=255, blank=True, null=True)
    choiceB_isCorrect=models.BooleanField(default=False)
    choiceC = models.CharField(max_length=255, blank=True, null=True)
    choiceC_isCorrect=models.BooleanField(default=False)
    isProblem = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True, )

    def __str__(self):
        return "%s" % self.questionBody

class UserQuizzes(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    created = models.DateTimeField(auto_now_add=True, )
    subject=models.ForeignKey(Subjects,on_delete=models.SET_NULL,related_name="subject_userquizzes",null=True)
    chapter=models.ForeignKey(Chapters,on_delete=models.SET_NULL,related_name="chapter_userquizzes",null=True)
    score=models.IntegerField(default=0,editable=False,)
# class choices(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.SET_NULL, related_name='choices_question', null=True,
#                                  blank=True)
#     choiceBody = models.CharField(max_length=70, blank=True, null=True)
#
#     def __str__(self):
#         if self.id==1:
#             return str(1)
#         elif self.id==2:
#             return str(2)
#         else:
#             return str(round((self.id-1)/self.id))
