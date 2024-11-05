from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomeTestCase(TestCase):
    def test_pagination_list(self):
        book = Book.objects.create(
            title="Book1", desc="desc1", isbn='11111111')
        user = CustomUser.objects.create(
            username='fazliddin',
            first_name="Fazliddin",
            last_name="Gadoyev",
            email='fazliddinn.gadoyev@gmail.com'
        )
        user.set_password('somepass')
        user.save()

        self.client.login(username='fazliddin', password='somepass')

        review1 = BookReview.objects.create(
            user=user,
            book=book,
            stars_given=5,
            comment="Very good book"
        )
        review2 = BookReview.objects.create(
            user=user,
            book=book,
            stars_given=4,
            comment="Useful book"
        )
        review3 = BookReview.objects.create(
            user=user,
            book=book,
            stars_given=3,
            comment="Nice book"
        )

        response = self.client.get(reverse('common:home_page') + '?per_page=2')

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)

