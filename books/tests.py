from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class BooksTestCase(TestCase):

    def test_no_books(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, "No book found.")

    def test_books_list(self):
        book1 = Book.objects.create(
            title="Book1", desc="desc1", isbn='11111111')
        book2 = Book.objects.create(
            title="Book2", desc="desc2", isbn='22222222')
        book3 = Book.objects.create(
            title="Book3", desc="desc3", isbn='33333333')

        response = self.client.get(reverse('books:list') + "?per_page=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(
            reverse('books:list') + '?page=2?per_page=2')

        self.assertContains(response, book3.title)

    def test_book_detail(self):
        book = Book.objects.create(
            title="Book1", desc='desc1', isbn='122121212')

        response = self.client.get(
            reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.desc)

    def test_search_books(self):
        book1 = Book.objects.create(
            title="History", desc="desc1", isbn='11111111')
        book2 = Book.objects.create(
            title="Lion", desc="desc2", isbn='22222222')
        book3 = Book.objects.create(
            title="Garbage", desc="desc3", isbn='33333333')

        response = self.client.get(reverse('books:list') + '?q=history')

        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?q=lion')

        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?q=garbage')

        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)


class EditReviewViewTestCase(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="Book1", desc="desc1", isbn='11111111')
        self.user = CustomUser.objects.create(
            username='fazliddin',
            first_name="Fazliddin",
            last_name="Gadoyev",
            email='fazliddinn.gadoyev@gmail.com'
        )
        self.user.set_password('somepass')
        self.user.save()

        self.client.login(username='fazliddin', password='somepass')

        self.review = BookReview.objects.create(
            user=self.user,
            book=self.book,
            stars_given=5,
            comment="Very good book"
        )

    def test_book_review_is_created(self):
        data = {
            'book': self.book,
            'user': self.user,
            'stars_given': 5,
            'comment': "nice book"
        }
        response = self.client.post(
            reverse('books:review',
                    kwargs={"id": self.book.id}
                    ),
            data=data
        )
        self.review.refresh_from_db()

        self.assertEqual(BookReview.objects.count(), 2)
        self.assertEqual(response.status_code, 302)

    def test_get_edit_review(self):
        response = self.client.get(
            reverse('books:edit-review', kwargs={'book_id': self.book.id, "review_id": self.review.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.review.comment)
        self.assertContains(response, self.review.stars_given)
        self.assertTemplateUsed(response, 'books/edit_review.html')

    def test_post_edit_review(self):
        data = {
            "comment": 'Very good book1',
            'stars_given': 4
        }
        response = self.client.post(reverse(
            'books:edit-review',
            kwargs={"book_id": self.book.id, "review_id": self.review.id}),
            data=data
        )

        self.review.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.review.comment, 'Very good book1')
        self.assertEqual(self.review.stars_given, 4)

    def test_get_confirm_delete_review(self):
        response = self.client.get(
            reverse('books:confirm-delete-review',
                    kwargs={"book_id": self.book.id, "review_id": self.review.id}
                    )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)
        self.assertContains(response, self.review.comment)

    def test_delete_review(self):
        response = self.client.get(
            reverse('books:delete-review', kwargs={"book_id": self.book.id, "review_id": self.review.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(BookReview.objects.count(), 0)
