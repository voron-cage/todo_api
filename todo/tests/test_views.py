import json

from django import test
from django.urls import reverse
from django.contrib.auth.models import User
from todo.models import TODOList, TODOAction


class TODOListViewSetTestCase(test.TestCase):
    def setUp(self) -> None:
        self.url = reverse('todo-list')
        self.user = User.objects.create(username='a')
        self.user.set_password('12345')
        self.user.save()
        self.client.login(username='a', password='12345')

    def test_create(self):
        data = {'title': 'Список дел'}
        resp = self.client.post(self.url, data=data)
        r_data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(r_data['id'], 0)
        self.assertEqual(r_data['title'], 'Список дел')
        self.assertEqual(r_data['slug'], 'spisok-del')
        self.assertEqual(r_data['user'], 1)
        self.assertEqual(r_data['action_count'], 0)


class TODOViewSetTestCase(test.TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='a')
        self.user.set_password('12345')
        self.user.save()
        self.todo = TODOList.objects.create(title='Список', slug='spisok', user=self.user)
        self.url = reverse('todo-detail', kwargs={'slug': 'spisok'})
        self.client.login(username='a', password='12345')

    def test_create_action(self):
        data = {'title': 'купить хлеб'}
        resp = self.client.post(self.url, data=data)
        r_data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(r_data['title'], 'купить хлеб')
        self.assertEqual(r_data['slug'], 'kupit-hleb')
        self.assertEqual(r_data['is_done'], False)

    def test_update(self):
        data = {'title': 'Список покупок', 'order': 3}
        resp = self.client.put(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        r_data = resp.json()
        self.assertEqual(r_data['title'], 'Список покупок')
        self.assertEqual(r_data['order'], 3)

    def test_delete_todo(self):
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(TODOList.objects.filter(pk=self.todo.pk).exists())


class TODOActionViewSetTestCase(test.TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='a')
        self.user.set_password('12345')
        self.user.save()
        self.todo = TODOList.objects.create(title='Список', slug='spisok', user=self.user)
        self.action = TODOAction.objects.create(title='Масло', slug='maslo', todo=self.todo)
        self.url = reverse('todo-action', kwargs={'slug': 'spisok', 'action_slug': 'maslo'})
        self.client.login(username='a', password='12345')

    def test_update(self):
        data = {'title': 'Творог', 'is_done': True}
        resp = self.client.put(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        r_data = resp.json()
        self.assertEqual(r_data['title'], 'Творог')
        self.assertEqual(r_data['is_done'], True)
        self.action.refresh_from_db()
        self.assertEqual(self.action.title, 'Творог')
        self.assertEqual(self.action.slug, 'tvorog')
        self.assertEqual(self.action.is_done, True)
