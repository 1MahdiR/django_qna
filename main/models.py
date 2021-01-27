from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):

    question_title = models.CharField(max_length=32, blank=True)
    question_user = models.ForeignKey(User,
    					on_delete=models.CASCADE,
    					related_name="user_question",
    					blank=True,null=True)
    question_date = models.DateTimeField(default=timezone.now)
    question_likes = models.IntegerField(default=0)
    question_text = models.TextField()

class Answer(models.Model):

    answer_user = models.ForeignKey(User,
    					on_delete=models.CASCADE,
    					related_name="user_answer",
    					blank=True,null=True)
    answer_likes = models.IntegerField(default=0)
    answer_text = models.TextField()
    answer_question = models.ForeignKey(Question,
                            on_delete=models.CASCADE,
                            related_name="question_answer",
                            blank=True,null=True)

