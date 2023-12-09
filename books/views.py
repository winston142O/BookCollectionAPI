from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import bookSerializer
from django.core.exceptions import ObjectDoesNotExist

# Use of decorator to establish that only authenticated users can access.
@permission_classes([IsAuthenticated])
class BookList(generics.ListCreateAPIView):
    serializer_class = bookSerializer

    # Retrieve list of books owned by the current user.
    def get_queryset(self):
        try:
            user = self.request.user
            if user is not None:
                queryset = Book.objects.filter(owner=user) # Currently authenticated user.
                title = self.request.query_params.get('title', None)
                author = self.request.query_params.get('author', None) 
                # Filter by title/author if required.               
                if title:
                    queryset = queryset.filter(title__icontains=title)
                if author:
                    queryset = queryset.filter(author__icontains=author)                
                return queryset
        except ValueError as ve:
            return Response({'error': f'Invalid value: {ve}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred while fetching book list'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Add book to collection
    def perform_create(self, serializer):
        try:
            serializer.save(owner=self.request.user) # Set currently authenticated user as book owner.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred while creating a book'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Use of decorator to establish that only authenticated users can access.
@permission_classes([IsAuthenticated])
class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = bookSerializer
    
    # Get book owned by current user.
    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user)

    # Update a book owned by current user.
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred while updating the book'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete a book owned by current user.
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred while deleting the book'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
