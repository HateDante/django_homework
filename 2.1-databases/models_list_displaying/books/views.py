from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import Book


def books_view(request):
    books_list = Book.objects.all()
    template = 'books/books_list.html'
    context = {'books': books_list}
    return render(request, template, context)


def book(request, pub_date):
    try:
        book_data = datetime.strptime(pub_date, '%Y-%m-%d').date()
    except TypeError:
        book_data = datetime.today()
    books_list = Book.objects.all().order_by('pub_date')
    paginator = Paginator(books_list, 1)
    page = 0
    for ind in range(books_list.count()):
        page = paginator.get_page(ind)
        current_book = page.object_list[0]
        if current_book.pub_date == book_data:
            break
    template = 'books/book.html'
    context = {'page': page}
    return render(request, template, context)
