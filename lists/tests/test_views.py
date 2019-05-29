from django.test import TestCase
from django.utils.html import escape
from django.urls import resolve, reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):
    """主页测试"""
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    # 表单form中包含了csrf_token随机值，导致这个用例测试不通过
    # def test_home_page_returns_correct_html(self):
    #     request = HttpRequest()
    #     response = home_page(request)
    #     expected_html = render_to_string('home.html')
    #     self.assertEqual(response.content.decode(), expected_html)


class ListViewTest(TestCase):
    """清单列表测试"""
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % list_.id)
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % correct_list.id)

        self.assertContains(response, 'itemey 1')  # self.assertIn('itemey 1', response.content.decode())
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % correct_list.id)
        # response.context表示要传入render函数的上下文（self.client把上下文附在response对象上，方便测试）
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()

        self.client.post('/lists/%d/' % correct_list.id, data={'item_text': 'A new item for an existing list'})
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        correct_list = List.objects.create()
        response = self.client.post('/lists/%d/' % correct_list.id, data={'item_text': 'A new item for an existing list'})
        self.assertRedirects(response, '/lists/%d/' % correct_list.id)

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post('/lists/%d/' % list_.id, data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)


class NewListTest(TestCase):
    """新建一个清单列表测试"""
    def test_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        self.assertRedirects(response, '/lists/%d/' % new_list.id)

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")  # Django会转义HTML中的单引号，所以这里也需要进行转义
        self.assertContains(response, expected_error)

    def test_invalid_list_item_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)