from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import BookReview


def landing_page(request):
    return render(request, 'index.html')


def home_page(request):
    book_reviews = BookReview.objects.all().order_by('-created_at')
    per_page = request.GET.get('per_page', 4)
    page_num = request.GET.get('page', 1)
    pagination = Paginator(book_reviews, per_page)
    page_obj = pagination.get_page(page_num)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'home.html', context)
