from django.urls import path
from .views import BookViews, BookInstanceViews, GenreViews
import uuid
urlpatterns = [
    path('genres/', GenreViews.as_view()),
    path('genres/<int:id>/', GenreViews.as_view()),
    path('books/<int:genre_id>/', BookViews.as_view()),
    path('books/', BookViews.as_view()),
    path('catalog/filter/<str:current_status>', BookInstanceViews.as_view()),
    path('catalog/', BookInstanceViews.as_view()),
    path('catalog/edit/', BookInstanceViews.as_view()),
    path('catalog/delete/<uuid:id>/', BookInstanceViews.as_view())
]
