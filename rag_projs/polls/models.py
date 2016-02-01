from __future__ import unicode_literals

from django.db import models
import os 
import datetime
from django.utils import timezone

#os.sys.path.append('/django_home/rag_projs/')

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return str(self.id) + ' : ' + self.question_text + ' : ' + str(self.pub_date) 

    def was_published_recently(self):
        return self.pub_date >  timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

# Create your models here.
