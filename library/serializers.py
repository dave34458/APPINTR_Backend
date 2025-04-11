from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, Borrow, AvailableBook, Review, CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class BookSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'published_date',
            'genre', 'isbn', 'description', 'language',
            'preview_image', 'is_available',
        ]

    def get_is_available(self, obj):
        for ab in obj.available_books.all():
            if not ab.borrows.filter(date_returned__isnull=True).exists():
                return True
        return False

class AvailableBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableBook
        fields = ['id', 'book', 'location']

class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['id', 'user', 'available_book', 'borrow_date', 'return_date', 'date_returned']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'comment']

