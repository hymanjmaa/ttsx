# -*- coding: utf-8 -*-
from haystack import indexes
from .models import GoodsInfo
__author__ = 'Hyman'
__time__ = '2017-08-04 16:19'


#指定对于某个类的某些数据建立索引
class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsInfo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
