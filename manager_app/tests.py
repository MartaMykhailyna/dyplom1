# manager_app/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from manager_app.models import Users

class UsersViewsTest(TestCase):

    def setUp(self):
        # Створення тестових даних
        self.user1 = Users.objects.create(id_user=1, name="User 1", u_status=False)
        self.user2 = Users.objects.create(id_user=2, name="User 2", u_status=True)
        self.client = Client()

    def test_users_view(self):
        # Отримання URL для в'юшки
        url = reverse('manager_app:users')

        # Виконання GET запиту до в'юшки
        response = self.client.get(url)

        # Перевірка статусу відповіді
        self.assertEqual(response.status_code, 200)

        # Перевірка використання правильного шаблону
        self.assertTemplateUsed(response, 'manager_app/users.html')

        # Перевірка наявності створених користувачів у контексті відповіді
        self.assertContains(response, "User 1")
        self.assertContains(response, "User 2")

    def test_users_toggle_status(self):
        # Отримання URL для зміни статусу користувача
        url = reverse('manager_app:users_toggle_status', args=[self.user1.id_user])

        # Виконання GET запиту до в'юшки
        response = self.client.get(url)

        # Перевірка редиректу після зміни статусу
        self.assertRedirects(response, reverse('manager_app:users'))

        # Перевірка, що статус користувача змінений
        self.user1.refresh_from_db()
        self.assertTrue(self.user1.u_status)

    def test_users_delete(self):
        # Отримання URL для видалення користувача
        url = reverse('manager_app:users_delete', args=[self.user1.id_user])

        # Виконання POST запиту до в'юшки
        response = self.client.post(url)

        # Перевірка редиректу після видалення
        self.assertRedirects(response, reverse('manager_app:users'))

        # Перевірка, що користувач видалений
        with self.assertRaises(Users.DoesNotExist):
            Users.objects.get(id_user=self.user1.id_user)
