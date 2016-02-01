from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    website = models.URLField()

    #def __unicode__(self):
    #    return self.name

class Author(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField('Last name', max_length=50)
    email = models.EmailField(blank=True, verbose_name='Email')

class Book(models.Model) :
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    pub_date = models.DateField()

# Create your models here.
