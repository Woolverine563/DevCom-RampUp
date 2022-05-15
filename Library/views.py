from django.shortcuts import render, get_object_or_404
import datetime
from .models import Action, Book, BookInstance, Genre
from django.http import JsonResponse
from .serializers import BookInstanceSerializer, BookSerializer, ActionSerializer, GenreSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.

class BookViews(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, genre_id=None):
        if genre_id:
            books = Book.objects.filter(genre__id=genre_id)
            serializer = BookSerializer(books, many=True)
            genre_name = Genre.objects.get(id=genre_id).name
            return Response({"status": "success", "genre": genre_name, "data": serializer.data}, status=status.HTTP_200_OK)
        items = Book.objects.all()
        serializer = BookSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class BookInstanceViews(APIView):
    def post(self, request):
        serializer = BookInstanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, current_status=None):
        if current_status:
            such_books = BookInstance.objects.filter(current_status=current_status)
            serializer =  BookInstanceSerializer(such_books, many=True)
            return Response({"status": "success", "data": serializer.data})

        items = BookInstance.objects.all()
        serializer = BookInstanceSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data})

    def patch(self, request):
        serializer = ActionSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data['action'] == 'borrow':
                copies = BookInstance.objects.filter(book__id=serializer.data['book_id'])
                for copy in copies:
                    if copy.current_status == 'a':
                        copy.current_status = 'o'
                        copy.due_back = datetime.date.today() + datetime.timedelta(days=60)
                        copy.save()
                        serializer = BookInstanceSerializer(copy)
                        return Response({"status": "Successfully loaned", "data": serializer.data})
                return Response({"status": "No copy for requested book available"})

            elif serializer.data['action'] == 'return':
                copy = BookInstance.objects.get(id=serializer.data['uuid'])
                if copy.current_status == 'o':
                    copy.current_status = 'a'
                    if copy.due_back >= datetime.date.today():
                        late = False
                    else:
                        late = True
                    print(copy.due_back)
                    copy.due_back = None
                    copy.save()
                    serializer = BookInstanceSerializer(copy)
                    if late:
                        return Response({"status": "The book was returned late", "data": serializer.data})
                    else:
                        return Response({"status": "Returned successfully", "data": serializer.data})
                return Response({"status": "Invalid return attempt"})

    def delete(self, request, id=None):
        to_delete = get_object_or_404(BookInstance, id=id)
        to_delete.delete()
        return Response({"status": "object deleted successfully"})    

class GenreViews(APIView):
    def get(self, request):
        items = Genre.objects.all()
        data = [f"{item.name}: {item.id}" for item in items]
        return Response({"status": "success", "data": data})
    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "successful", "data": serializer.data})
        return Response({"status": "failed"})
    
    



                


        

