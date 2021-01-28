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
    question_likes = models.ManyToManyField(User, related_name="user_question_likes")
    question_dislikes = models.ManyToManyField(User, related_name="user_question_dislikes")
    question_text = models.TextField()

    def question_likes_count(self):
        return self.question_likes.count()

    def question_dislikes_count(self):
        return self.question_dislikes.count()

class Answer(models.Model):

    answer_user = models.ForeignKey(User,
    					on_delete=models.CASCADE,
    					related_name="user_answer",
    					blank=True,null=True)
    answer_likes = models.ManyToManyField(User, related_name="user_answer_likes")
    answer_dislikes = models.ManyToManyField(User, related_name="user_answer_dislikes")
    answer_text = models.TextField()
    answer_question = models.ForeignKey(Question,
                            on_delete=models.CASCADE,
                            related_name="question_answer",
                            blank=True,null=True)

    def answer_likes_count(self):
        return self.answer_likes.count()

    def answer_dislikes_count(self):
        return self.answer_dislikes.count()
