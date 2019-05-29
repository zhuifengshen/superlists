from django.db import models
from django.urls import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField(default='')
    # 反向查询（reverse lookup)：Django自动创建反向关系，related_name默认为（class_name)_set
    # 这里表示List实例可以通过item_set访问这个清单的item列表
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
