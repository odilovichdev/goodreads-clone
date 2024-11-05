from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):

    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                "username": "fazliddin",
                "first_name": "Fazliddin",
                "last_name": "Gadoyev",
                "email": "fazliddinn.gadoyev@gmail.com",
                "password1": "somepassword",
                "password2": "somepassword"
            })
        user = CustomUser.objects.get(username='fazliddin')

        self.assertEquals(user.first_name, "Fazliddin")
        self.assertEquals(user.last_name, "Gadoyev")
        self.assertEquals(user.username, "fazliddin")
        self.assertEquals(user.email, 'fazliddinn.gadoyev@gmail.com')
        self.assertNotEquals(user.password, 'somepassword')
        self.assertTrue(user.check_password("somepassword"))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name': "Fazliddin",
                'email': "fazliddinn.gadoyev@gmail.com"
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)

        form = response.context.get('form')

        self.assertFormError(form, 'username', 'This field is required.')
        self.assertFormError(form, 'password1', 'This field is required.')
        self.assertFormError(form, 'password2', 'This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                "first_name": "Fazliddin",
                "last_name": "Gadoyev",
                "username": "fazliddin",
                "email": 'invalid email',
                'password1': "somepassword",
                'password2': 'somepassword'
            }
        )

        user_count = CustomUser.objects.count()
        form = response.context['form']

        self.assertEqual(user_count, 0)
        self.assertFormError(form, 'email', "Enter a valid email address.")

    def test_unique_username(self):
        user = CustomUser.objects.create(username='fazliddin')
        user.set_password('somepass')
        user.save()

        response = self.client.post(
            reverse('users:register'),
            data={
                "first_name": "Fazliddin",
                "last_name": "Gadoyev",
                "username": "fazliddin",
                "email": 'fazliddinn.gadoyev@gail.com',
                'password1': "somepassword",
                'password2': 'somepassword'
            }
        )

        user_count = CustomUser.objects.count()
        form = response.context.get('form')

        self.assertEqual(user_count, 1)
        self.assertFormError(form, 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):

    def setUp(self):
        self.db_user = CustomUser.objects.create(username="fazliddin", first_name='Fazliddin')
        self.db_user.set_password("somepass")
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                "username": 'fazliddin',
                "password": 'somepass'
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('users:login'),
            data={
                "username": 'wrong-username',
                "password": 'somepass'
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                "username": 'fazliddin',
                "password": 'wrong-username'
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username='fazliddin', password='somepass')
        self.client.get(reverse('users:logout'))

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='fazliddin',
            first_name='Fazliddin',
            last_name='Gadoyev',
            email='fazliddinn.gadoyev@gmail.com'
        )
        self.user.set_password('somepass')
        self.user.save()

    def test_login_required(self):
        response = self.client.post(reverse('users:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login') + '?next=/users/profile/')

    def test_profile_details(self):
        self.client.login(username='fazliddin', password='somepass')

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)

    def test_profile_update(self):
        self.client.login(username='fazliddin', password='somepass')

        response = self.client.post(reverse('users:profile-edit'),
                                    data={
                                        'username': "fazliddin",
                                        'first_name': 'Fazliddinn',
                                        'last_name': "Gadoyev1",
                                        'email': 'fazliddinn.gadoyev@gmail.com'
                                    })

        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, "Fazliddinn")
        self.assertEqual(self.user.last_name, "Gadoyev1")
        self.assertEqual(self.user.username, "fazliddin")
        self.assertEqual(self.user.email, "fazliddinn.gadoyev@gmail.com")
        self.assertEqual(response.url, reverse('users:profile'))
