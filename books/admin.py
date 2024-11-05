from django.contrib import admin

from books.models import Book, Author, BookReview, BookAuthor


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = 'title', 'isbn', 'desc'
    list_filter = 'title',
    search_fields = 'title','isbn'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    pass