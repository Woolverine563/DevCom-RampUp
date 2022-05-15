from optparse import AmbiguousOptionError
from django.contrib import admin
from .models import Book, BookInstance, Genre, User
# Register your models here.

admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(User)