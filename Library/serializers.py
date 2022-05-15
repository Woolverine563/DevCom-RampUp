
from rest_framework import serializers
from .models import Book, User, Genre, BookInstance, Action

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['action', 'book_id', 'uuid']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre']
    def to_representation(self, instance):
        response = super().to_representation(instance)
        genres = instance.genre.all()
        response['genre'] = [one_genre.name for one_genre in genres]
        return response

class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = ['book', 'id', 'current_status', 'due_back']
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['book'] = BookSerializer(instance.book).data
        LOAN_STATUS = {
            'm': 'Maintenance',
            'o': 'On loan',
            'a': 'Available',
            'r': 'Reserved',
        }
        complete = LOAN_STATUS[instance.current_status]
        response['current_status'] = complete
        return response 