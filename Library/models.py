from django.db import models
from django.urls import reverse
import uuid
# Create your models here.

class Action(models.Model):
    action = models.CharField(max_length=10, null=False)
    uuid = models.UUIDField(null=True)
    book_id = models.IntegerField(null=True)

class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name
    
class User(models.Model):
    name = models.CharField(max_length=100, blank=False)
    books = models.ManyToManyField('BookInstance')
    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100, blank=False)
    genre = models.ManyToManyField(Genre)
    author = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self) -> str:
        return self.title

class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, blank=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    current_status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
    )
    def __str__(self) -> str:
        return f'{self.book, (self.id)}'

