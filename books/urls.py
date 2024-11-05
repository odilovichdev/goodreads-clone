from django.urls import path

from books.views import BookListView, BookDetailView, BookReviewView, EditReviewView, ConfirmDeleteReviewView, \
    DeleteReviewView

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('<int:id>/', BookDetailView.as_view(), name='detail'),
    path('<int:id>/review/', BookReviewView.as_view(), name='review'),
    path("<int:book_id>/reviews/<int:review_id>/edit/", EditReviewView.as_view(), name="edit-review"),
    path(
        "<int:book_id>/reviews/<int:review_id>/delete/confirm/",
        ConfirmDeleteReviewView.as_view(),
        name='confirm-delete-review'
    ),
    path(
        "<int:book_id>/reviews/<int:review_id>/delete/",
        DeleteReviewView.as_view(),
        name='delete-review'
    )
]
